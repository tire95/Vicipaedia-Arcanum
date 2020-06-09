# Vicipaedia Arcanum - Tietosanakirja pöytäroolipeleille

Vicipaedia Arcanum (tästä lähtien *VA*) on nettipalvelimella toimiva tietosanakirja pöytäroolipeleille. *VA*:ssa käyttäjä voi luoda omalle pelilleen kampanjan, liittyä muiden luomiin kampanjoihin, ja päivittää kampanjaan liittyvää tietokantaa hirviöistä ja NPC:stä (non-player character).

Kun kampanja luodaan, se voidaan suojata salasanalla, jotta vain tietyt käyttäjät voivat liittyä siihen. Kampanjaan liittyneet käyttäjät voivat vapaasti lisätä ja muokata kampanjan sisällä olevia entiteettejä. Kampanjan luojalla on kampanjassa admin-oikeudet, eli hän voi poistaa muita käyttäjiä kampanjasta ja halutessaan myös poistaa koko kampanjan.

Tällä hetkellä *VA*:ssa voit:

* luoda käyttäjätilin
* kirjautua käyttäjätilille
* luoda kampanjan
* rekisteröityä muiden tekemiin kampanjoihin
* katsoa kampanjan hirviö- ja NPC-listoja
* lisätä, muokata ja poistaa hirviöitä ja NPC:tä
* (kampanjan luojana) poistaa henkilöitä kampanjasta
* (kampanjan luojana) poistaa kampanjan

[Linkki Heroku-pilvipalvelimella pyörivään sovellukseen](https://vicipaedia-arcanum.herokuapp.com/)

## [User storyt](https://github.com/tire95/Vicipaedia-Arcanum/tree/master/documentation/user_stories.md)

## Tietokantakaavio

![kaavio](/documentation/Pictures/DBDiagram.png)

## Asennusohje

1. Varmista, että sinulla on asennettuna [vähintään Pythonin versio 3.5](https://www.python.org/downloads/) sekä Pythonin [pip](https://packaging.python.org/key_projects/#pip) (asentuu tavallisesti Pythonin kanssa) ja [venv-kirjasto](https://docs.python.org/3/library/venv.html)
2. Aktivoi kansiossa ´/Vicipaedia-Arcanum/venv/Scripts´ oleva tiedosto ´activate.bat´
3. Navigoi terminaalissa projektin juurikansioon ja syötä komento ´pip install -r requirements.txt´; näin pip asentaa tarvittavat kirjastot
4. Käynnistä ohjelma suorittamalla tiedosto ´run.py´

## Käyttöohje

1. Kun navigoit sovelluksen aloitusosoitteeseen (lokaalisti http://localhost:5000/), klikkaa oikeassa yläkulmassa olevaa nappia "Login or register"
2. Avautuvassa ikkunassa voit rekisteröityä sovellukseen oikeanpuoleisella lomakkeella (kaikissa lomakkeissa on ohjeistukset oikeanlaiseen syötteeseen)
3. Kun olet rekisteröitynyt, voit kirjautua sisään vasemmanpuoleisella lomakkeella
4. Kirjauduttuasi avautuu näkymä, jossa ylhäällä on linkkeinä kaikki kampanjat, joihin olet liittynyt, sen alapuolella näkyy lista kaikista kampanjoista, joihin et ole liittynyt, ja ylhäällä olevassa valikossa on uutena vaihtoehtona "Create a campaign"
5. Painamalla "Create a campaign" pääset näkymään, jossa voit luoda uuden kampanjan. Luotuasi kampanjan olet kampanjan admin
6. Kun haluat liittyä kampanjaan, palvelu kysyy kampanjan salasanaa (jos kampanjalla on salasana). Syöttäessäsi salasanan oikein (tai jos kampanjalla ei ole salasanaa) palvelu rekisteröi sinut kampanjaan ja pääset kampanjan valikkoon
7. Kampanjan valikossa on kaksi "korttia"; vasemmanpuoleinen Creatures ja oikeanpuoleinen NPCs. Korttien alapuolella näkyy myös kuinka monta kyseistä entiteettiä kampanjassa on
8. Kun valitset joko Creatures tai NPCs kohdassa 7, pääset listaan, jossa näkyy kampanjan kaikki kyseiset entiteetit. Täällä voit etsiä entiteettiä, muokata tai postaa tietyn entiteetin, tai lisätä uuden entiteetin
9. Kampanjan adminina voit hallinnoida kampanjaa. Kun menet kampanjan valikkoon, näet ylhäällä napin "Manage Campaign". Tästä pääset näkymään, jossa voit poistaa käyttäjiä kampanjasta tai poistaa koko kampanjan (kampanjan poistamiseen sinun pitää syöttää kampanjan nimi ja salasana, jotta et vahingossa poistaisi kampanjaa)