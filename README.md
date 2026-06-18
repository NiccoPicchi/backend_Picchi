# Piccomerce REST API

**Studente:** Niccolò Picchi  
**Tipo progetto:** REST API  
**Framework:** Django + Django REST Framework  

---

## Descrizione

Piccomerce è una piattaforma e-commerce che permette la gestione di prodotti, categorie, carrello e ordini. Il sistema supporta due ruoli utente: customer e manager, con permessi differenziati per ogni operazione.

---

## Funzionalità per ruolo

Il sistema prevede due ruoli applicativi (campo `role` sul modello utente: `customer`, `manager`) più l'account amministratore, che corrisponde al superuser Django e non è un valore del campo `role` (per coerenza gli è stato assegnato il valore `manager`).

### Customer
- Registrazione e login
- Visualizzazione e filtraggio categorie e prodotti disponibili (ovvero prodotti con campo `available` messo a true)
- Gestione del carrello (aggiunta, modifica quantità, rimozione, svuotamento)
- Creazione ordini dal carrello
- Visualizzazione e cancellazione dei propri ordini (solo se in stato PENDING)
- Gestione del proprio profilo

### Manager
- Registrazione e login
- Operazioni di lettura, creazione, modifica ed eliminazione di prodotti e categorie
- Visualizzazione di tutti gli ordini (con filtro per stato)
- Aggiornamento dello stato degli ordini

### Admin (superuser)
- Accesso al pannello di amministrazione degli utenti (`Admin Panel`)
- Gestione completa degli utenti tramite il client (creazione, aggiornamento, eliminazione) dalla sezione dedicata
- Accesso a tutte le funzionalità riservate al manager e ai customer

---

## Installazione locale

```
# 1. Clona il repository e apri la cartella clientInterface

# 2. Apri il file api_client.html su un browser per testare tutte le funzionalità
```

---

## Database demo

Il file `db.sqlite3` incluso nel repository contiene dati pre-popolati pronti per il testing.

### Account demo

| Username | Password | Ruolo |
|---|---|---|
| admin_demo | admin12345 | manager |
| manager_demo | manager12345 | manager |
| customer_demo | customer12345 | customer |
| customer2_demo | customer12345 | customer |

### Dati inclusi
- 3 categorie (Elettronica, Abbigliamento, Casa e Cucina)
- 8 prodotti (di cui 1 esaurito nella categoria Abbigliamento)
- 4 ordini in stati diversi (DELIVERED, SHIPPED, PENDING, CANCELLED)
- Carrello riempito per customer_demo, vuoto per customer2_demo
- Ordini DELIVERED e SHIPPED per customer_demo, PENDING e CANCELLED per customer2_demo

---

## Client di test

Apri il file `api_client.html` direttamente nel browser. Non richiede installazione aggiuntiva.

Il client permette di testare tutte le operazioni disponibili: autenticazione, gestione profilo, categorie, prodotti, carrello e ordini.

---

## Endpoint

| Metodo | URL | Auth | Ruolo | Descrizione |
|---|---|---|---|---|
| POST | `/api/auth/register/` | No | — | Registrazione nuovo utente |
| POST | `/api/auth/login/` | No | — | Login, restituisce token |
| POST | `/api/auth/logout/` | Sì | Tutti | Invalida il token |
| GET | `/api/auth/profile/` | Sì | Tutti | Visualizza profilo |
| PATCH | `/api/auth/profile/` | Sì | Tutti | Aggiorna profilo |
| GET | `/api/auth/users/` | Sì | Admin | Lista utenti |
| POST | `/api/auth/users/create/` | Sì | Admin | Crea nuovo utente |
| GET | `/api/auth/users/{id}/` | Sì | Admin | Dettaglio utente |
| PATCH | `/api/auth/users/{id}/` | Sì | Admin | Aggiorna utente (ruolo, email, stato attivo) |
| DELETE | `/api/auth/users/{id}/` | Sì | Admin | Elimina utente |
| GET | `/api/catalog/categories/` | No | — | Lista categorie |
| POST | `/api/catalog/categories/` | Sì | Manager, Admin | Crea categoria |
| GET | `/api/catalog/categories/{id}/` | No | — | Dettaglio categoria |
| PUT/PATCH | `/api/catalog/categories/{id}/` | Sì | Manager, Admin | Modifica categoria |
| DELETE | `/api/catalog/categories/{id}/` | Sì | Manager, Admin | Elimina categoria |
| GET | `/api/catalog/products/` | No | — | Lista prodotti (filtri: name, category, category_name, id, ordering) |
| POST | `/api/catalog/products/` | Sì | Manager, Admin | Crea prodotto |
| GET | `/api/catalog/products/{id}/` | No | — | Dettaglio prodotto |
| PUT/PATCH | `/api/catalog/products/{id}/` | Sì | Manager, Admin | Modifica prodotto |
| DELETE | `/api/catalog/products/{id}/` | Sì | Manager, Admin | Elimina prodotto |
| GET | `/api/shop/cart/` | Sì | Customer, Admin | Visualizza carrello |
| POST | `/api/shop/cart/` | Sì | Customer, Admin | Aggiunge prodotto al carrello |
| DELETE | `/api/shop/cart/` | Sì | Customer, Admin | Svuota carrello |
| PATCH | `/api/shop/cart/{item_id}/` | Sì | Customer, Admin | Modifica quantità item |
| DELETE | `/api/shop/cart/{item_id}/` | Sì | Customer, Admin | Rimuove item dal carrello |
| GET | `/api/shop/orders/` | Sì | Tutti | Lista ordini (propri per customer, tutti per manager) |
| POST | `/api/shop/orders/` | Sì | Customer, Admin | Crea ordine dal carrello |
| GET | `/api/shop/orders/{id}/` | Sì | Tutti | Dettaglio ordine |
| PATCH | `/api/shop/orders/{id}/` | Sì | Manager, Admin | Aggiorna stato ordine |
| DELETE | `/api/shop/orders/{id}/` | Sì | Customer, Admin | Cancella ordine (solo PENDING) |

---

## Deployment

Link deployment: https://piccomerce-production.up.railway.app

---

## Struttura del progetto

```
ecommerce_api/          # configurazione principale (settings, urls)
accounts/               # autenticazione, utenti, permessi
catalog/                # prodotti e categorie
orders/                 # carrello e ordini
clientInterface/
  api_client.html         # client di test browser
  style.css               # stile client
  script.js               # logica client
db.sqlite3              # database demo pre-popolato
requirements.txt
runtime.txt
README.md
Procfile
```
