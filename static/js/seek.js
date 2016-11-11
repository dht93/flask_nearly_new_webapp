function getRandomIntInclusive(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
var arr1=['Whatever you seek, yo. Books, xeroxed notes, anything.',
'eg. Computer Networks (6th sem) xerox notes','eg. Introduction to Algorithms, 3rd. Ed, by CLRS',
'eg. Computer Networks by Tanenbaum','Whatever you want, yo!',
'eg. 6 months old Raspberry Pi',
'eg. 6 months old Arduino Uno Board','eg. Big-ass poster of The Dark Knight','eg. Curtains',
'eg. Blanket','eg. Table Lamp','eg. Laptop Speakers','eg. The Cuckoo\'s Calling By Robert Galbraith',
'eg. Steve Jobs by Walter Isaccson',
"eg. A Tale of Two Cities by Charles Dickens",
"eg. The Lord of the Rings (The Lord of the Rings, #1-3) by J.R.R. Tolkien",
"eg. The Hobbit by J.R.R. Tolkien",
"eg. The Dream of the Red Chamber by Cao Xueqin",
"eg. And Then There Were None by Agatha Christie",
"eg. The Lion, the Witch, and the Wardrobe (Chronicles of Narnia, #1) by C.S. Lewis",
"eg. She (She, #1) by H. Rider Haggard",
"eg. The Da Vinci Code (Robert Langdon, #2) by Dan Brown",
"eg. Think and Grow Rich by Napoleon Hill",
"eg. The Catcher in the Rye by J.D. Salinger",
"eg. The Alchemist by Paulo Coelho",
"eg. Steps to Christ by Ellen G. White",
"eg. Lolita by Vladimir Nabokov",
"eg. Heidi (Heidi, #1) by Johanna Spyri",
"eg. Baby and Child Care by Benjamin Spock",
"eg. Anne of Green Gables (Anne of Green Gables, #1) by L.M. Montgomery",
"eg. Black Beauty by Anna Sewell",
"eg. The Name of the Rose by Umberto Eco",
"eg. The Eagle Has Landed (Liam Devlin, #1) by Jack Higgins",
"eg. Watership Down by Richard Adams",
"eg. The Hite Report by Shere Hite",
"eg. Charlotte's Web by E.B. White",
"eg. The Ginger Man by J.P. Donleavy",
"eg. The Tale of Peter Rabbit by Beatrix Potter",
"eg. Harry Potter and the Deathly Hallows (Harry Potter, #7) by J.K. Rowling",
"eg. Jonathan Livingston Seagull by Richard Bach",
"eg. A Message to Garcia by Elbert Hubbard",
"eg. Sophie's World by Jostein Gaarder",
"eg. Angels & Demons  (Robert Langdon, #1) by Dan Brown",
"eg. How the Steel Was Tempered by Nikolai Ostrovsky",
"eg. War and Peace by Leo Tolstoy",
"eg. Pinocchio by Carlo Collodi",
"eg. You Can Heal Your Life by Louise L. Hay",
"eg. Kane and Abel (Kane and Abel, #1) by Jeffrey Archer",
"eg. The Diary of a Young Girl by Anne Frank",
"eg. In His Steps by Charles M. Sheldon",
"eg. To Kill a Mockingbird by Harper Lee",
"eg. Valley of the Dolls by Jacqueline Susann",
"eg. Gone with the Wind by Margaret Mitchell",
"eg. The Purpose Driven Life: What on Earth Am I Here for? by Rick Warren",
"eg. The Thorn Birds by Colleen McCullough",
"eg. The Revolt of Mamie Stover by William Bradford Huie",
"eg. The Girl with the Dragon Tattoo (Millennium, #1) by Stieg Larsson",
"eg. The Very Hungry Caterpillar by Eric Carle",
"eg. The Late Great Planet Earth by Hal Lindsey",
"eg. Who Moved My Cheese? by Spencer Johnson",
"eg. The Wind in the Willows by Kenneth Grahame",
"eg. 1984 by George Orwell",
"eg. The 7 Habits of Highly Effective People: Powerful Lessons in Personal Change by Stephen R. Covey",
"eg. The Celestine Prophecy (Celestine Prophecy, #1) by James Redfield",
"eg. The Hunger Games (The Hunger Games, #1) by Suzanne Collins",
"eg. The Godfather by Mario Puzo",
"eg. Love Story (Love Story, #1) by Erich Segal",
"eg. Wolf Totem by Jiang Rong",
"eg. The Happy Hooker: My Own Story by Xaviera Hollander",
"eg. Jaws by Peter Benchley",
"eg. Love You Forever by Robert Munsch",
"eg. The Women's Room by Marilyn French",
"eg. What to Expect When You're Expecting by Heidi Murkoff",
"eg. The Adventures of Huckleberry Finn (Tom Sawyer & Huckleberry Finn, #2) by Mark Twain",
"eg. The Secret Diary of Adrian Mole, Aged 13 3/4  (Adrian Mole, #1) by Sue Townsend",
"eg. Kon-Tiki by Thor Heyerdahl",
"eg. Where the Wild Things Are by Maurice Sendak",
"eg. The Secret (The Secret, #1) by Rhonda Byrne",
"eg. Fear of Flying by Erica Jong",
"eg. The Shack by Wm. Paul Young",
"eg. Goodnight Moon by Margaret Wise Brown",
"eg. The Neverending Story by Michael Ende",
"eg. Guess How Much I Love You by Sam McBratney",
"eg. The Poky Little Puppy by Janette Sebring Lowrey",
"eg. The Pillars of the Earth  (The Pillars of the Earth, #1) by Ken Follett",
"eg. How to Win Friends and Influence People by Dale Carnegie",
"eg. The Grapes of Wrath by John Steinbeck",
"eg. The Horse Whisperer by Nicholas Evans",
"eg. The Hitchhiker's Guide to the Galaxy (Hitchhiker's Guide to the Galaxy, #1) by Douglas Adams",
"eg. Tuesdays with Morrie by Mitch Albom",
"eg. God's Little Acre by Erskine Caldwell",
"eg. Follow Your Heart by Susanna Tamaro",
"eg. The Outsiders by S.E. Hinton",
"eg. Charlie and the Chocolate Factory (Charlie Bucket, #1) by Roald Dahl",
"eg. Norwegian Wood by Haruki Murakami",
"eg. Peyton Place by Grace Metalious",
"eg. Dune (Dune Chronicles, #1) by Frank Herbert",
"eg. The Plague by Albert Camus",
"eg. No Longer Human by Osamu Dazai",
"eg. The Naked Ape: A Zoologist's Study of the Human Animal by Desmond Morris",
"eg. The Bridges of Madison County by Robert James Waller",
"eg. Man's Search for Meaning by Viktor E. Frankl",
"eg. The Divine Comedy by Dante Alighieri",
"eg. Things Fall Apart (The African Trilogy, #1) by Chinua Achebe",
"eg. The Prophet by Kahlil Gibran",
"eg. The Exorcist by William Peter Blatty",
"eg. The Gruffalo by Julia Donaldson",
"eg. Catch-22 by Joseph Heller",
"eg. Eye of the Needle by Ken Follett"]
var arr2=['eg. Willing to shell out around 300 bucks','eg. Willing to shell out around 500 bucks','eg. Willing to shell out around 400 bucks']

function inp1in(){
  text=arr1[getRandomIntInclusive(0,arr1.length-1)];
  document.getElementById('inp1').innerHTML='&nbsp;&nbsp;'+text;
  document.getElementById('inp1').style.display='inline';
}

function inp1out(){
  document.getElementById('inp1').style.display='none';
}

function inp2in(){
  text=arr2[getRandomIntInclusive(0,arr2.length-1)];
  document.getElementById('inp2').innerHTML='&nbsp;&nbsp;'+text;
  document.getElementById('inp2').style.display='inline';
}

function inp2out(){
  document.getElementById('inp2').style.display='none';
}
