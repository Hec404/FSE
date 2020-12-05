//Puedes seguir el proceso para construir este juego con el siguiente tuturial
//https://youtu.be/ZniVgo8U7ek

//Arreglo de todas las cartas
const cards = document.querySelectorAll('.memory-card');

let hasFlippedCard = false;
let lockBoard = false;
let firstCard, secondCard;

//Función que permite voltear la carta
function flipCard(){
   //Si el tablero está bloqueado o si se dio doble clic a la carta
   //retorna inmediatamente
  if (lockBoard || this === firstCard) return;


  //Agrega o quita la clase flip al elemento que invocó la acción
  this.classList.toggle('flip');

  //Si no se ha volteado la carta previamente
  if (!hasFlippedCard){ //Se ha volteado la primer carta
    hasFlippedCard = true;
    firstCard = this;
  } else { //Se ha volteado la segunda carta
    hasFlippedCard = false;
    secondCard = this;

    checkForMatch(); //Revisa si las cartas son iguales
  }
}

function checkForMatch(){
  let isMatch = firstCard.dataset.framework === secondCard.dataset.framework;
  //Si los datos de las cartas coinciden, se desactiva el volver a usarlas
  //En caso contrario, no se voltea la segunda carta
  isMatch ? disableCards() : unFlipCards();
}

function disableCards(){
  firstCard.removeEventListener('click', flipCard);
  secondCard.removeEventListener('click', flipCard);
}

function unFlipCards(){
  lockBoard = true; //Bloquea el tablero
  setTimeout( () => { //Timeout para permitir ver la segunda carta
    firstCard.classList.remove('flip');
    secondCard.classList.remove('flip');
    resetBoard();
  }, 1500);
}

function resetBoard(){
  hasFlippedCard = lockBoard = false;
  firstCard = secondCard = null;
}

// Función para asignar un número aleatorio a la propiedad "order" de todas
// las cartas, lo cual permite ordenar de forma aleatoria las cartas
(function shuffle(){
  cards.forEach(card => {
    let randomPos = Math.floor(Math.random() * 12);
    card.style.order = randomPos;
  });
})();

//Para cada carta, se agrega un listener que se invoca cada que se da clic en la
//carta
cards.forEach(card => card.addEventListener('click',flipCard));
