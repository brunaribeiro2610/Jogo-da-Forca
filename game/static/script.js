document.addEventListener('DOMContentLoaded', () => {
  console.log('script.js: DOMContentLoaded')
  const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('')
  const keyboardEl = document.getElementById('keyboard')
  const maskedEl = document.getElementById('masked')
  const messageEl = document.getElementById('message')
  const resetBtn = document.getElementById('reset')

  if(!keyboardEl || !maskedEl || !messageEl || !resetBtn){
    console.warn('Elementos do DOM não encontrados — script abortado:', {keyboardEl, maskedEl, messageEl, resetBtn})
    return
  }

  console.log('script.js: elementos principais encontrados, criando teclado')

  // getCookie no escopo superior para ser usado por tryLetter e reset
  function getCookie(name){
    const v = document.cookie.match('(^|;)\\s*'+name+'\\s*=\\s*([^;]+)')
    return v ? v.pop() : ''
  }

  letters.forEach(l => {
    const btn = document.createElement('button')
    btn.className = 'key'
    btn.textContent = l
    btn.addEventListener('click', () => { console.log('click', l); tryLetter(l, btn) })
    keyboardEl.appendChild(btn)
  })

  console.log('script.js: teclado criado com', document.querySelectorAll('.key').length, 'teclas')

  async function fetchState(){
    try{
    const res = await fetch('/state/', {credentials: 'same-origin'})
      if(!res.ok) throw new Error('status:'+res.status)
      return await res.json()
    }catch(err){
      console.error('fetchState erro', err)
      return {word:'',masked:'',correct:[],wrong:[],errors:0,finished:false}
    }
  }

  function showParts(errors){
    const parts = document.querySelectorAll('svg .part')
    parts.forEach((p,i)=>{
      if(i<errors) p.classList.add('show')
      else p.classList.remove('show')
    })
  }

  async function refresh(){
    const s = await fetchState()
    maskedEl.textContent = s.masked.split('').join(' ')
    document.querySelectorAll('.key').forEach(k=>{
      if(s.correct.includes(k.textContent) || s.wrong.includes(k.textContent)){
        k.classList.add('disabled')
        k.disabled=true
      }
    })
    showParts(s.errors)
    if(s.finished){
      if(s.masked===s.word){
        messageEl.textContent='Você venceu! 🎉'
        messageEl.className='message win'
      }else{
        messageEl.textContent=`Você perdeu. Palavra: ${s.word}`
        messageEl.className='message lose'
      }
    }else{
      messageEl.textContent=''
      messageEl.className='message'
    }
  }

  async function tryLetter(letter, btn){
    if(btn.disabled) return
    // usar getCookie definida no escopo superior
    let data = null
    try{
      console.log('tryLetter: enviando', letter)
      const res = await fetch('/guess/',{
        method:'POST',
        credentials: 'same-origin',
        headers:{'Content-Type':'application/json','X-CSRFToken': getCookie('csrftoken')},
        body: JSON.stringify({letter})
      })
      if(!res.ok){
        console.error('tryLetter: resposta não OK', res.status)
        const text = await res.text()
        console.error('tryLetter body:', text)
        messageEl.textContent = 'Erro no servidor'
        return
      }
      data = await res.json()
      console.log('tryLetter: resposta', data)
      if(!data.ok){
        messageEl.textContent=data.msg||''
        setTimeout(()=>{messageEl.textContent=''},1200)
        return
      }
    }catch(err){
      console.error('tryLetter fetch erro', err)
      messageEl.textContent='Erro na rede'
      return
    }
    btn.classList.add('disabled')
    btn.disabled=true
    if(data.win || data.lose){
      if(data.win) maskedEl.textContent = data.masked.split('').join(' ')
      if(data.lose) maskedEl.textContent = data.word.split('').join(' ')
      showParts(data.errors)
    }
    await refresh()
  }

  resetBtn.addEventListener('click', async ()=>{
  await fetch('/reset/',{method:'POST', credentials: 'same-origin', headers: {'X-CSRFToken': getCookie('csrftoken')}})
    document.querySelectorAll('.key').forEach(k=>{k.classList.remove('disabled');k.disabled=false})
    messageEl.textContent=''
    showParts(0)
    await refresh()
  })

  refresh()
})
