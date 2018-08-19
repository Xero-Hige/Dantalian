class DbBaseHandler:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.open_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def open_connection(self):
        pass

    def close_connection(self):
        pass

    def _get_cursor(self):
        pass
