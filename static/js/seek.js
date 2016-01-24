function getRandomIntInclusive(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
var arr1=['Whatever you seek, yo. Books, xeroxed notes, anything.','eg. Computer Networks (6th sem) xerox notes','eg. Introduction to Algorithms, 3rd. Ed, by CLRS','eg. Computer Networks by Tanenbaum','Whatever you want, yo!']
var arr2=['eg. Willing to shell out around 300 bucks','eg. Willing to shell out around 500 bucks','eg. Willing to shell out around 400 bucks']

function inp1in(){
  text=arr1[getRandomIntInclusive(0,arr1.length-1)];
  console.log(text);
  document.getElementById('inp1').innerHTML='&nbsp;&nbsp;'+text;
  document.getElementById('inp1').style.display='inline';
}

function inp1out(){
  document.getElementById('inp1').style.display='none';
}

function inp2in(){
  text=arr2[getRandomIntInclusive(0,arr2.length-1)];
  console.log(text);
  document.getElementById('inp2').innerHTML='&nbsp;&nbsp;'+text;
  document.getElementById('inp2').style.display='inline';
}

function inp2out(){
  document.getElementById('inp2').style.display='none';
}
