#include <LiquidCrystal.h>
#include <SPI.h>
#include <SD.h>


// =======================
// LCD
// =======================

const int rs = 2;
const int en = 3;
const int d4 = 6;
const int d5 = 7;
const int d6 = 8;
const int d7 = 9;

LiquidCrystal lcd(rs,en,d4,d5,d6,d7);

// =======================
// INPUT
// =======================

const int xPin = A1;
const int yPin = A2;
const int switchPin = 5;

// =======================
// SD
// =======================

const int chipSelect = 10;

// =======================
// Button
// =======================

const int buttonPin = 4;

// =======================
// MENU
// =======================

enum State
{
  ALBUM_MENU,
  SONG_MENU,
  LYRICS
};

State state = ALBUM_MENU;

// =======================
// MEMORY SAFE STORAGE
// =======================

#define MAX_ALBUMS 58
#define MAX_SONGS 27


char albumName[42];
char albumFolder[8];

char songNames[MAX_SONGS][17];

int albumIndex = 0;
int songIndex = 0;

int totalSongs = 0;

unsigned long lastMove = 0;

// =======================
// SETUP
// =======================

void setup()
{

Serial.begin(9600);


lcd.begin(16,2);


pinMode(switchPin,INPUT_PULLUP);
pinMode(buttonPin, INPUT_PULLUP);


lcd.clear();
lcd.print("Starting...");



if(!SD.begin(chipSelect))
{

lcd.clear();
lcd.print("SD ERROR");

while(1);

}



delay(1000);



loadAlbum();


}

// =======================
// LOOP
// =======================

void loop()
{


if(state == ALBUM_MENU)
{
albumMenu();
}


else if(state == SONG_MENU)
{
songMenu();
}


else if(state == LYRICS)
{
playLyrics();
}


}

// =======================
// ALBUM MENU - Makes album titles display
// =======================

void albumMenu()
{

  static int scrollPos = 0;
  static unsigned long lastScroll = 0;

  int len = strlen(albumName);


  lcd.setCursor(0,0);

  // Clear row
  lcd.print("                ");

  lcd.setCursor(0,0);

  // Arrow
  lcd.print(">");


  // First row has 15 chars after arrow
  for(int i = 0; i < 31; i++)
  {
    int index = scrollPos + i;

    if(index < len)
      lcd.print(albumName[index]);
    else
      lcd.print(" ");
  }



  lcd.setCursor(0,1);

  // Clear second row
  lcd.print("                ");

  lcd.setCursor(0,1);


  // Second row starts at character 15
  for(int i = 15; i < 31; i++)
  {

    int index = scrollPos + i;

    if(index < len)
      lcd.print(albumName[index]);
    else
      lcd.print(" ");

  }

  // Scroll long titles
  static unsigned long pauseStart = 0;
  static bool scrolling = false;
  
  if(len > 31){

    if(!scrolling){
      // wait before starting scroll
      if(millis() - pauseStart > 1500){
        scrolling = true;
        lastScroll = millis();
      }
    }
    else{
      if(millis()-lastScroll > 300){

        scrollPos++;

        if(scrollPos > len - 31){
          scrollPos = 0;
          scrolling = false;
          pauseStart = millis();
        }

        lastScroll = millis();
      }
    }
  }
  else{
    scrollPos = 0;
    scrolling = false;
    pauseStart = millis();
  }



  joystickAlbum();



  if(digitalRead(switchPin)==LOW)
  {

    delay(300);

    loadSongs();

    state = SONG_MENU;

    lcd.clear();

  }

}

// =======================
// SONG MENU - Makes song titles display
// =======================

void songMenu()
{

static int lastSongIndex = -1;


if(songIndex != lastSongIndex){
  lcd.clear();
  lastSongIndex = songIndex;
}

lcd.setCursor(0,0);

// Display track number
lcd.print(songIndex + 1);
lcd.print(".");

lcd.print(songNames[songIndex]);

// Controls 

joystickSong();



if(digitalRead(switchPin)==LOW)
{

delay(300);

state=LYRICS;

lcd.clear();

}

if(digitalRead(buttonPin)==LOW){

  delay(300);

  state=ALBUM_MENU;

  lcd.clear();
}

}

// =======================
// JOYSTICK ALBUM
// =======================


void joystickAlbum()
{


if(millis()-lastMove <350)
return;



int x = analogRead(xPin);



if(x < 300)
{

albumIndex++;

if(albumIndex>=MAX_ALBUMS)
albumIndex=0;


loadAlbum();

lastMove=millis();

}



if(x >700)
{

if(albumIndex==0)
albumIndex=MAX_ALBUMS-1;

else
albumIndex--;


loadAlbum();

lastMove=millis();

}


}

// =======================
// JOYSTICK SONG
// =======================


void joystickSong()
{


if(millis()-lastMove <350)
return;


int x=analogRead(xPin);



if(x<300)
{

songIndex++;

if(songIndex>=totalSongs)
songIndex=0;


lcd.clear();

lastMove=millis();

}



if(x>700)
{

songIndex--;

if(songIndex<0)
songIndex=totalSongs - 1;


lcd.clear();

lastMove=millis();

}


}

// =======================
// LOAD ALBUM FROM CATALOG
// =======================
void loadAlbum()
{

File f=SD.open("catalog.txt");

int count=0;

while(f.available())
{

String line=f.readStringUntil('\n');


if(count==albumIndex)
{


int a=line.indexOf('|');

int b=line.indexOf('|',a+1);

String id=line.substring(0,a);

String title=line.substring(a+1,b);

title.toCharArray(albumName,64);

fixLCD(albumName);

sprintf(albumFolder,"ALB%s",id.c_str());


break;

}


count++;

}


f.close();


lcd.clear();


}

// =======================
// LOAD SONGS
// =======================

void loadSongs()
{
String path=String(albumFolder)+"/tracks.txt";


Serial.print("Folder: ");
Serial.println(albumFolder);
Serial.print("Path: ");
Serial.println(path);

File f = SD.open(path);

Serial.println(f ? "File opened OK" : "File FAILED to open");


int i=0;

while(f.available() && i<MAX_SONGS)
{

String line=f.readStringUntil('\n');

line.trim();

if(line.length()==0) continue;

int split=line.indexOf('|');

if(split==-1) continue;

String title=line.substring(split+1);

title.trim();

title.toCharArray(songNames[i],17);

fixLCD(songNames[i]);

i++;

}

f.close();

totalSongs = i;

songIndex = 0;

}

// =======================
// PLAY TIMED LYRICS
// =======================
void playLyrics()
{

String path =
String(albumFolder)+
"/T"+
String(songIndex+1)+
".txt";

File lyric = SD.open(path);

if(!lyric)
{

lcd.print("NO LYRICS");

delay(2000);

state=SONG_MENU;

return;

}

unsigned long lastTime = 0;

while(lyric.available())
{

String line =
lyric.readStringUntil('\n');

int first=line.indexOf('|');

int second=line.indexOf('|',first+1);

if(first==-1)
continue;

String timestamp =
line.substring(0,first);


String row1 =
line.substring(first+1,second);

String row2 =
line.substring(second+1);

row1.trim();
row2.trim();
timestamp.trim();

row1.toCharArray(albumName,64);
fixLCD(albumName);
row1 = String(albumName);

row2.toCharArray(albumName, 64);
fixLCD(albumName);
row2 = String(albumName);

unsigned long currentTime = parseTime(timestamp);
unsigned long waitTime = currentTime - lastTime;
lastTime = currentTime;


if (waitTime > 0)
    delay(waitTime);
else
    delay(800);


lcd.clear();
lcd.setCursor(0,0);
lcd.print(row1);
lcd.setCursor(0,1);
lcd.print(row2);


}

delay(3000);

lyric.close();

state=SONG_MENU;

lcd.clear();

}

// =======================
// TIMESTAMP PARSER
// =======================
unsigned long parseTime(String t)
{

int colon=t.indexOf(':');

int dot=t.indexOf('.');

int min=t.substring(0,colon).toInt();

int sec=t.substring(colon+1,dot).toInt();

int ms=t.substring(dot+1).toInt();

return ((unsigned long)(min*60+sec))*1000UL + ms*10UL;

}

// =======================
// LCD CHARACTER FIX
// =======================
void fixLCD(char *text)
{

for(int i=0; text[i] != '\0'; i++)
{

// UTF-8 Spanish characters
if((unsigned char)text[i] == 0xC3)
{

i++;

switch((unsigned char)text[i])
{

case 0xA1: text[i-1]='a'; text[i]='\0'; break; // á
case 0xA9: text[i-1]='e'; text[i]='\0'; break; // é
case 0xAD: text[i-1]='i'; text[i]='\0'; break; // í
case 0xB3: text[i-1]='o'; text[i]='\0'; break; // ó
case 0xBA: text[i-1]='u'; text[i]='\0'; break; // ú

case 0x81: text[i-1]='A'; text[i]='\0'; break; // Á
case 0x89: text[i-1]='E'; text[i]='\0'; break; // É
case 0x8D: text[i-1]='I'; text[i]='\0'; break; // Í
case 0x93: text[i-1]='O'; text[i]='\0'; break; // Ó
case 0x9A: text[i-1]='U'; text[i]='\0'; break; // Ú

case 0xB1: text[i-1]='n'; text[i]='\0'; break; // ñ
case 0x91: text[i-1]='N'; text[i]='\0'; break; // Ñ

}

}

}

}