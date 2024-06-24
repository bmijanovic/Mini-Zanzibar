# Mini-Zanzibar

## Analiza sistema

### 1. Funkcionalnosti sistema
- Prijava na sistem
- Kreiranje belih tabli
- Deljenje belih tabli sa drugim korisnicima (kao posmatrač ili kao urednik)
- Uklanjanje dozvola za pristup
- Izmena belih tabli
- Brisanje belih tabli

### 2. Komponente sistema
- Mini Zanzibar - Komponenta za autorizaciju koja upravlja pravima pristupa.
- Klijent - aplikacija za rad sa belim tablama
    - Whiteboard aplikacija - Front-end aplikacija 
    - Server - Back-end aplikacija 

## Definisanje bezbedonosnih zahteva (prema OWASP ASVS)

### V2 Autentikacija:

- ASVS 2.1: Obezbeđena lozinka doboljno velike dužine.
- ASVS 2.3: Implementirano sigurno čuvanje lozinki (npr. hashing sa bcrypt).

### V3 Upravljanje sesijama:

- ASVS 3.1: Koristišćene sigurne metode za upravljanje sesijama - secured cookies
- ASVS 3.2: Implementirane sesije sa vremenskim ograničenjem i automatskim istekom.
- ASVS 3.3: Osiguratno je da sesije budu pravilno invalidirane nakon odjave korisnika.

### V4 Kontrola pristupa:

- ASVS 4.1: Definisane i implementirane granularne kontrole pristupa koristeći Zanzibar model.
- ASVS 4.2: Verifikovano da korisnici mogu pristupiti samo onim resursima za koje imaju eksplicitna prava.

### V5 Validacija, sanitizacija i enkodiranje:

- ASVS 5.1: Svi osjetljivi podaci su enkriptovani tokom prenosa i u mirovanju.
- ASVS 5.3: Čuvano minimalno potrebnih podataka i brisani nepotrebni podaci na siguran način.

### V6 Kriptografija:

- ASVS 6.1: Implementirani validacioni mehanizmi za sve ulazne podatke.
- ASVS 6.2: Zaštićen sistem od napada putem unosa.
- ASVS 6.4: Osetljivi podaci čuvani u .env fajlovima

### V7 Upravljanje greškama:

- ASVS 7.4: Osigurano da se greške pravilno rukovode i da ne otkrivaju osjetljive informacije korisnicima.

