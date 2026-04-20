# Karum

**Take control of your finances**

Karum is a financial aggregation system that helps you track and control
all your assets in one place --- including bank accounts,
cryptocurrencies, and future investment portfolios.

Instead of manually tracking transactions, Karum connects to external
services and builds a unified financial view automatically.

------------------------------------------------------------------------

## ✨ Features

-   📊 Unified financial overview (fiat + crypto)
-   🔌 Integration with external providers (APIs, exchanges, banks)
-   ⚡ Automatic data synchronization
-   🧠 Designed for scalability (Clean Architecture)
-   🔒 Secure and self-hosted

------------------------------------------------------------------------

## 🏗️ Tech Stack

-   Python 3.12+
-   FastAPI
-   PostgreSQL
-   SQLAlchemy (async)
-   Alembic

------------------------------------------------------------------------

## ⚙️ Setup

### 1. Clone repository

``` bash
git clone https://github.com/QuaronSoftware/karum-finance.git
cd karum-finance
```

------------------------------------------------------------------------

### 2. Create `.env`

Create a `.env` file in the root directory:

.env.example

------------------------------------------------------------------------

### 3. Install dependencies

Using `uv`:

``` bash
uv sync
```

------------------------------------------------------------------------

## 🗄️ Migrations

Run database migrations:

``` bash
export DATABASE_URL="postgresql+asyncpg://user:pass@localhost/dbname" && alembic upgrade head
```

------------------------------------------------------------------------

## 🚀 Run

### Development

``` bash
uv run uvicorn karum.main:main --app-dir src --reload --factory
```

------------------------------------------------------------------------

### Production

``` bash
uv run uvicorn karum.main:main --app-dir src --factory
```

------------------------------------------------------------------------

## 📁 Project Structure

    src/karum/
      config/           # settings .env
      domain/           # core business logic
      application/      # use cases & services
      infra/            # db, providers, external APIs
      delivery/         # API / routers
      shared/           # utils

------------------------------------------------------------------------

## 🧠 Philosophy

Karum is built around a simple idea:

> Stop tracking. Start controlling.

The system is designed to: - minimize manual input - aggregate financial
data automatically - provide a single source of truth for all assets

------------------------------------------------------------------------

## 🔮 Roadmap

-   [ ] Bank integrations
-   [ ] Crypto exchanges (OKX, Bybit, etc.)
-   [ ] Portfolio analytics
-   [ ] Web UI (React)
-   [ ] Alerts & automation

------------------------------------------------------------------------

## 🤝 Contributing

Contributions are welcome.

Feel free to open issues or submit pull requests.

------------------------------------------------------------------------

## 📜 License

MIT License