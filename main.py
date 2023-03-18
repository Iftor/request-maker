from app.src.services import RequestService


if __name__ == "__main__":
    print(f"Запросов обработано: {RequestService.run()}")
