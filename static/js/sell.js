function getRandomIntInclusive(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
var arr1=['Whatever you wanna sell, yo. Books, xeroxed notes, anything.','eg. Computer Networks (6th sem) xerox notes','eg. Introduction to Algorithms, 3rd. Ed, by CLRS','eg. Computer Networks by Tanenbaum','Whatever you wanna sell, yo!']
var arr2=['Enter 0 if you wanna give away for free!',"eg. 300/-. Or you may write 0 if you're willing to give away for free."]
var arr3=['eg. 6 months','eg. 1 year', 'eg. 2 years','eg. just bought it!','eg. 4 months']
var arr4=['eg. In pretty good shape!','eg. Works like a charm!','eg. Scribblings on some pages',"eg. I'm givin' it away for free but I expect a coffee in return!"]

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

function inp3in(){
  text=arr3[getRandomIntInclusive(0,arr3.length-1)];
  console.log(text);
  document.getElementById('inp3').innerHTML='&nbsp;&nbsp;'+text;
  document.getElementById('inp3').style.display='inline';
}

function inp3out(){
  document.getElementById('inp3').style.display='none';
}
function inp4in(){
  text=arr4[getRandomIntInclusive(0,arr4.length-1)];
  console.log(text);
  document.getElementById('inp4').innerHTML='&nbsp;&nbsp;'+text;
  document.getElementById('inp4').style.display='inline';
}

function inp4out(){
  document.getElementById('inp4').style.display='none';
}
