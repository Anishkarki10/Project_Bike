const menuButton=document.querySelector('[data-menu-button]');const mobileMenu=document.querySelector('[data-mobile-menu]');if(menuButton&&mobileMenu){menuButton.addEventListener('click',()=>mobileMenu.classList.toggle('hidden'));}
document.querySelectorAll('[data-bike-thumb]').forEach(btn=>{btn.addEventListener('click',()=>{const main=document.querySelector('[data-main-bike-image]');if(main)main.src=btn.dataset.bikeThumb;});});
setTimeout(()=>document.querySelectorAll('.fixed.top-20').forEach(x=>x.remove()),4500);
