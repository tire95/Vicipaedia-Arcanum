# Vicipaedia Arcanum - Tietosanakirja pöytäroolipeleille

Sisällysluettelo:
* [Kuvaus](#kuvaus)
* [Tietokanta](#tietokanta)
* [Käyttötapaukset ja niihin liittyvät kyselyt](#käyttötapaukset-ja-niihin-liittyvät-kyselyt)
* [Asennusohje](#asennusohje)
* [Käyttöohje](#käyttöohje)
   - [Rekisteröityminen ja sisäänkirjautuminen](#rekisteröityminen-ja-sisäänkirjautuminen)
   - [Kampanjan luominen](#kampanjan-luominen)
   - [Kampanjaan liittyminen](#kampanjaan-liittyminen)
   - [Entiteettien lisääminen kampanjaan](#entiteettien-lisääminen-kampanjaan)
   - [Entiteettien muokkaaminen](#entiteettien-muokkaaminen)
   - [Entiteettien poistaminen](#entiteettien-poistaminen)
   - [Kampanjan hallinnointi](#kampanjan-hallinnointi)
* [Rajoitteet](#rajoitteet)
* [Jatkokehitysideat](#jatkokehitysideat)

## Kuvaus

Vicipaedia Arcanum (tästä lähtien *VA*) on nettipalvelimella toimiva tietosanakirja pöytäroolipeleille. *VA*:ssa käyttäjä voi luoda omalle pelilleen kampanjan, liittyä muiden luomiin kampanjoihin, ja päivittää kampanjaan liittyvää tietokantaa hirviöistä ja NPC:istä (non-player character).

Kun kampanja luodaan, se voidaan suojata salasanalla, jotta vain tietyt käyttäjät voivat liittyä siihen. Kampanjaan liittyneet käyttäjät voivat vapaasti lisätä ja muokata kampanjan sisällä olevia entiteettejä. Kampanjan luojalla on kampanjassa admin-oikeudet, eli hän voi poistaa muita käyttäjiä, hirviöitä ja NPC:itä kampanjasta, vaihtaa kampanjan salasanan, ja poistaa koko kampanjan.

Tällä hetkellä *VA*:ssa voit:

* luoda käyttäjätilin
* kirjautua käyttäjätilille
* luoda kampanjan
* rekisteröityä muiden tekemiin kampanjoihin
* katsoa kampanjan hirviö- ja NPC-listoja
* lisätä ja muokata hirviöitä ja NPC:itä
* (kampanjan luojana) poistaa hirviöitä ja NPC:itä
* (kampanjan luojana) poistaa henkilöitä kampanjasta
* (kampanjan luojana) vaihtaa kampanjan salasanan
* (kampanjan luojana) poistaa kampanjan

[Linkki Heroku-pilvipalvelimella pyörivään sovellukseen](https://vicipaedia-arcanum.herokuapp.com/)

## Tietokanta

![kaavio](/documentation/Pictures/DBDiagram.png)

CREATE TABLE -lauseet:

    CREATE TABLE account (
            id INTEGER NOT NULL,
            date_created DATETIME,
            date_modified DATETIME,
            name VARCHAR(144) NOT NULL,
            password VARCHAR(144) NOT NULL,
            PRIMARY KEY (id)
    );
    CREATE TABLE campaign (
            id INTEGER NOT NULL,
            date_created DATETIME,
            date_modified DATETIME,
            campaign_name VARCHAR(144) NOT NULL,
            game_system VARCHAR(144) NOT NULL,
            password VARCHAR(144),
            admin_id INTEGER NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY(admin_id) REFERENCES account (id)
    );
    CREATE TABLE creature (
            id INTEGER NOT NULL,
            date_created DATETIME,
            date_modified DATETIME,
            creature_name VARCHAR(144) NOT NULL,
            type VARCHAR(144) NOT NULL,
            size VARCHAR(144) NOT NULL,
            description VARCHAR(1000),
            campaign_id INTEGER NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY(campaign_id) REFERENCES campaign (id) ON DELETE CASCADE
    );
    CREATE TABLE association (
            account_id INTEGER,
            campaign_id INTEGER,
            FOREIGN KEY(account_id) REFERENCES account (id),
            FOREIGN KEY(campaign_id) REFERENCES campaign (id)
    );
    CREATE TABLE npc (
            id INTEGER NOT NULL,
            date_created DATETIME,
            date_modified DATETIME,
            npc_name VARCHAR(144) NOT NULL,
            race VARCHAR(144) NOT NULL,
            location VARCHAR(144) NOT NULL,
            occupation VARCHAR(144) NOT NULL,
            description VARCHAR(1000),
            campaign_id INTEGER NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY(campaign_id) REFERENCES campaign (id) ON DELETE CASCADE
    );


## Käyttötapaukset ja niihin liittyvät kyselyt

1. "Haluan suojata luomani kampanjan salasanalla, jotta vain haluamani henkilöt voivat liittyä siihen."

   Tarkistetaan, onko kyseisellä nimellä kampanjaa:

        SELECT * FROM campaign WHERE campaign_name LIKE "%campaign_name%";

   Kampanjan luominen, jos kyseisellä nimellä ei ole kampanjaa:

        INSERT INTO campaign (date_created, date_modified, campaign_name, game_system, password) VALUES (current_date, current_date, campaign_name, game_system, password);

2. "Opimme jotain uutta Beholderista, mutta Beholder on jo lisätty kampanjamme listaan. Tämän vuoksi haluan, että hirviöiden tietoja voi muokata helposti."

   Jos halutaan muuttaa nimeä, tarkistetaan, onko uudella nimellä hirviötä (tai NPC:tä):

        SELECT * FROM creature WHERE creature_name LIKE "%creature_name%" AND creature.campaign_id = campaign_id;

   Hirviön (tai NPC:n) muuttaminen:

        UPDATE creature SET date_modified = current_date, creature_name = new_name, type = new_type, size = new_size, description = new_description WHERE id = id;

3. "Pelaan useammassa kampanjassa, minkä vuoksi haluan pystyä liittymään useampaan kampanjaan palvelussa."

   Uuden liitoksen luominen liitostauluun:

        INSERT INTO association (account_id, campaign_id) VALUES (current_user_id, campaign_id);

4. "Haluan pitää eri kampanjoissa oppimani tiedot erillään toisistaan, koska kampanjoiden hirviöt voivat poiketa toisistaan paljonkin."

   Tiettyyn kampanjaan liittyvien NPC:iden (tai hirviöiden) hakeminen:

        SELECT * FROM npc WHERE npc.campaign_id = campaign_id;

5. "Haluan helposti nähdä kampanjat, joihin olen jo liittynyt."

   Kampanjat, joihin käyttäjä on liittynyt, sekä näiden lukumäärä:

        SELECT * FROM campaign INNER JOIN association ON campaign.id = association.campaign_id AND association.account_id = current_user_id;

        SELECT COUNT(campaign.id) FROM campaign INNER JOIN association ON campaign.id = association.campaign_id AND association.account_id = current_user_id;

6. "Kaverini loi kampanjan palveluun. Haluan, että kampanjan voi etsiä nimellä, jotta kampanjaan liittyminen olisi helppoa ja nopeaa."

7. "Kohtasin pelissä zombien näköisen otuksen, mutta en ole varma, oliko kyseessä zombie. Tämän vuoksi haluan, että palvelussa voi etsiä hirviöitä nimen ja tyypin perusteella."

Kohtien 6 ja 7 toiminnallisuus on toteutettu front endissä.

## Asennusohje

1. Varmista, että sinulla on asennettuna [vähintään Pythonin versio 3.5](https://www.python.org/downloads/) sekä Pythonin [pip](https://packaging.python.org/key_projects/#pip) (asentuu tavallisesti Pythonin kanssa) ja [venv-kirjasto](https://docs.python.org/3/library/venv.html)
2. Luo kansioon virtuaaliympäristö komennolla

         python3 -m venv venv
      
3. Aktivoi kansiossa `/Vicipaedia-Arcanum/venv/Scripts` oleva tiedosto `activate.bat` (Linuxilla riittää komento `source venv/bin/activate`)
4. Navigoi terminaalissa projektin juurikansioon ja syötä komento `pip install -r requirements.txt`; näin pip asentaa tarvittavat kirjastot
5. Käynnistä sovellus suorittamalla tiedosto `run.py`. Sovellus pyörii nyt lokaalisti koneellasi, tietokannanhallinnassa käytetään SQLiteä, ja debug-muoto on päällä
6. Halutessasi sovellus on valmis siirrettäväksi pilveen. Tiedostossa `__init__.py` voit muokata, mitä tietokannanhallintajärjestelmää käytetään. Tällä hetkellä on määritelty, että Herokussa käytetään PostgreSQL:ää seuraavalla koodilla

         if os.environ.get("HEROKU"):
            app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

## Käyttöohje

Sovelluksessa on jokaisessa input-kentässä ohjeet oikeanlaiselle syötteelle, joten näitä ei käsitellä ohjeissa. Lisäksi sovellus ilmoittaa mahdollisista virheistä/ongelmista syötteessä.

### Rekisteröityminen ja sisäänkirjautuminen

1. Navigoi selaimellasi sovelluksen aloitusosoitteeseen (lokaalisti http://localhost:5000/)
2. Klikkaa oikeassa yläkulmassa olevaa vaihtoehtoa "Login or register"
3. Avautuvassa ikkunassa voit rekisteröityä sovellukseen oikeanpuoleisella lomakkeella. Syötä käyttäjänimi ja salasana, ja paina nappia "Register"
4. Kun olet rekisteröitynyt, voit kirjautua sisään vasemmanpuoleisella lomakkeella

### Kampanjan luominen

1. Kirjauduttuasi sisään avautuu näkymä kampanjoista, joihin olet liittynyt
2. Luodaksesi uuden kampanjan paina ylävalikossa olevaa vaihtoehtoa "Create a campaign"
3. Syötä tarvittavat tiedot ja paina nappia "Create a new campaign"
4. Uusi kampanja on luotu, ja olet sen admin

### Kampanjaan liittyminen

1. Kirjauduttuasi sisään sivun yläosassa on linkki "Click here for more campaigns." Tätä painamalla pääsee listaan, jossa näkyy kaikki kampanjat, joihin et ole liittynyt
2. Etsi kampanjaa nimen tai pelisysteemin perusteella taulukon oikeassa yläkulmassa olevalla hakukentällä
3. Paina nappia "Join campaign"
4. a) Jos kampanjalla ei ole salasanaa, olet automaattisesti rekisteröitynyt kampanjaan
4. b) Jos kampanjalla on salasana, avautuu uusi näkymä. Syötä salasana ja paina "Join campaign"

### Entiteettien lisääminen kampanjaan

1. Kampanjan valikossa on kaksi "korttia"; vasemmanpuoleinen Creatures ja oikeanpuoleinen NPCs. Korttien alapuolella näkyy kuinka monta kyseistä entiteettiä kampanjassa on
2. Valitse joko Creatures tai NPCs klikkaamalla kuvaa tai näiden alapuolella olevaa tekstiä
3. Näkymässä on taulukkona kampanjan kaikki kyseiset entiteetit. Paina taulukon yläpuolella olevaa linkkiä "Add *entiteetti*"
4. Syötä tarvittavat tiedot ja paina nappia "Add a new *entiteetti*"

### Entiteettien muokkaaminen

1. Etsi entiteettiä taulukosta hakukentällä
2. Paina nappia "Open *entiteetti*"
3. Näkymässä näet entiteetin kaikki tiedot. Paina nappia "Modify *entiteetti*"

### Entiteettien poistaminen

1. Huom. poistaminen vaatii kampanjan admin-oikeudet
2. Kun avaat entiteetin, "Modify *entiteetti*" napin vieressä on nappi "Delete *entiteetti*"

### Kampanjan hallinnointi

1. Huom. kampanjan hallinnointi vaatii kampanjan admin-oikeudet
2. Kun avaat kampanjan, ylhäällä on nappi "Manage campaign"
2. Painamalla nappia pääset näkymään, jossa voit poistaa muita käyttäjiä kampanjasta painamalla nappia "Remove account from campaign"
3. Painamalla "Change password" pääset näkymään, jossa voit vaihtaa kampanjan salasanaa. Syötä tarvittavat tiedot ja paina nappia "Change password"
4. Painamalla "Delete campaign" avautuu näkymä, jossa pyydetään kampanjan nimeä ja salasanaa. Syötä nämä ja paina nappia "Delete campaign"

## Rajoitteet

1. Käyttäjä ei tällä hetkellä voi vaihtaa salasanaansa
2. Käyttäjä ei voi palauttaa unohtamaansa salasanaa
3. Palvelussa ei ole yleistä admin-käyttäjää, joka voisi poistaa muita käyttäjiä
4. Kampanjan tietoja ei voi muuttaa

## Jatkokehitysideat

1. Kampanjan luomisessa/muokkaamisessa checkbox, jonka avulla päättää, onko kampanjalla salasanaa. Näin kampanjalta voi myöhemmin poistaa salasana
2. Yleisiä hirviöitä, jotka lisätään kampanjaan (pelisysteemin mukaan?)
