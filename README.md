# Vicipaedia Arcanum - Tietosanakirja pöytäroolipeleille

Vicipaedia Arcanum (tästä lähtien *VA*) on nettipalvelimella toimiva tietosanakirja pöytäroolipeleille. *VA*:ssa käyttäjä voi luoda omalle pelilleen kampanjan, liittyä muiden luomiin kampanjoihin, ja päivittää kampanjaan liittyvää tietokantaa hirviöistä ja NPC:istä (non-player character).

Kun kampanja luodaan, se voidaan suojata salasanalla, jotta vain tietyt käyttäjät voivat liittyä siihen. Kampanjaan liittyneet käyttäjät voivat vapaasti lisätä ja muokata kampanjan sisällä olevia entiteettejä. Kampanjan luojalla on kampanjassa admin-oikeudet, eli hän voi poistaa muita käyttäjiä kampanjasta ja halutessaan myös poistaa koko kampanjan.

Tällä hetkellä *VA*:ssa voit:

* luoda käyttäjätilin
* kirjautua käyttäjätilille
* luoda kampanjan
* rekisteröityä muiden tekemiin kampanjoihin
* katsoa kampanjan hirviö- ja NPC-listoja
* lisätä, muokata ja poistaa hirviöitä ja NPC:itä
* (kampanjan luojana) poistaa henkilöitä kampanjasta
* (kampanjan luojana) poistaa kampanjan

[Linkki Heroku-pilvipalvelimella pyörivään sovellukseen](https://vicipaedia-arcanum.herokuapp.com/)

## [User storyt](https://github.com/tire95/Vicipaedia-Arcanum/tree/master/documentation/user_stories.md)

## Tietokantakaavio

![kaavio](/documentation/Pictures/DBDiagram.png)

## Asennusohje

1. Varmista, että sinulla on asennettuna [vähintään Pythonin versio 3.5](https://www.python.org/downloads/) sekä Pythonin [pip](https://packaging.python.org/key_projects/#pip) (asentuu tavallisesti Pythonin kanssa) ja [venv-kirjasto](https://docs.python.org/3/library/venv.html)
2. Aktivoi kansiossa `/Vicipaedia-Arcanum/venv/Scripts` oleva tiedosto `activate.bat`
3. Navigoi terminaalissa projektin juurikansioon ja syötä komento `pip install -r requirements.txt`; näin pip asentaa tarvittavat kirjastot
4. Käynnistä sovellus suorittamalla tiedosto `run.py`. Sovellus pyörii nyt lokaalisti koneellasi

## Käyttöohje

Sovelluksessa on jokaisessa input-kentässä ohjeet oikeanlaiselle syötteelle, joten näitä ei käsitellä ohjeissa. Lisäksi sovellus ilmoittaa mahdollisista virheistä/ongelmista syötteessä.

### Rekisteröityminen ja sisäänkirjautuminen

1. Navigoi selaimellasi sovelluksen aloitusosoitteeseen (lokaalisti http://localhost:5000/)
2. Klikkaa oikeassa yläkulmassa olevaa vaihtoehtoa "Login or register"
3. Avautuvassa ikkunassa voit rekisteröityä sovellukseen oikeanpuoleisella lomakkeella. Syötä käyttäjänimi ja salasana, ja paina nappia "Register"
4. Kun olet rekisteröitynyt, voit kirjautua sisään vasemmanpuoleisella lomakkeella

### Kampanjan luominen

1. Kirjauduttuasi sisään avautuu näkymä sovelluksessa olevista kampanjoista. Sivun yläosassa on listattuna kaikki kampanjat, joihin olet liittynyt. Tämän alapuolella näkyy lista kaikista kampanjoista, joihin et ole liittynyt
2. Luodaksesi uuden kampanjan paina ylävalikossa olevaa vaihtoehtoa "Create a campaign"
3. Syötä tarvittavat tiedot ja paina nappia "Create a new campaign"
4. Uusi kampanja on luotu, ja olet sen admin

### Kampanjaan liittyminen

1. Kirjauduttuasi sisään sivun alaosassa olevassa taulukossa näkyy lista kampanjoista, joihin et ole liittynyt
2. Etsi kampanjaa nimen tai pelisysteemin perusteella taulukon oikeassa yläkulmassa olevalla hakukentällä
3. Paina nappia "Join campaign"
4. a) Jos kampanjalla ei ole salasanaa, olet automaattisesti rekisteröitynyt kampanjaan
4. b) Jos kampanjalla on salasana, avautuu uusi näkymä. Syötä salasana ja paina "Join campaign"

### Entiteettien lisääminen kampanjaan

1. Kampanjan valikossa on kaksi "korttia"; vasemmanpuoleinen Creatures ja oikeanpuoleinen NPCs. Korttien alapuolella näkyy kuinka monta kyseistä entiteettiä kampanjassa on
2. Valitse joko Creatures tai NPCs klikkaamalla kuvaa tai näiden alapuolella olevaa tekstiä
3. Näkymässä on taulukkona kampanjan kaikki kyseiset entiteetit. Paina taulukon yläpuolella olevaa linkkiä "Add *entiteetti*"
4. Syötä tarvittavat tiedot ja paina nappia "Add a new *entiteetti*"

### Entiteettien muokkaaminen ja poistaminen

1. Etsi entiteettiä taulukosta hakukentällä
2. Paina nappia "Open *entiteetti*"
3. Näkymässä näet entiteetin kaikki tiedot. Paina nappia "Modify *entiteetti*" tai "Remove *entiteetti*"

### Kampanjan admin

1. Kampanjan adminina, kun avaat kampanjan, ylhäällä on nappi "Manage campaign"
2. Painamalla nappia pääset näkymään, jossa voit poistaa muita käyttäjiä kampanjasta painamalla nappia "Remove account from campaign"
3. Painamalla "Delete campaign" avautuu näkymä, jossa pyydetään kampanjan nimeä ja salasanaa. Syötä nämä ja paina nappia "Delete campaign"