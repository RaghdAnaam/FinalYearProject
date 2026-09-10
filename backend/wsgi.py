from app import create_app
import logging

app = create_app()
app.config["DEBUG"] = False  # Disable debug mode in production

# Set logging to INFO level (reduce spam)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
app.logger.info("Flask is starting...")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)


