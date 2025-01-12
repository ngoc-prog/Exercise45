import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6 import uic


class BookManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load file UI từ Qt Designer
        uic.loadUi("MainWindow.ui", self)

        # Dữ liệu mẫu cho danh sách sách
        self.books = [
            {"ISBN": "112", "Title": "Basic Python", "Author": "Trần Thanh Thân", "Year": 2020, "Publisher": "VNU"},
            {"ISBN": "113", "Title": "Advance Python", "Author": "Nguyễn Văn A", "Year": 2020, "Publisher": "ABC"},
            {"ISBN": "114", "Title": "Machine learning", "Author": "Lê Hoàng", "Year": 2024, "Publisher": "VNU"},
            {"ISBN": "115", "Title": "Django", "Author": "Hoàng Yến", "Year": 2023, "Publisher": "VNU"},
            {"ISBN": "111", "Title": "Mobile", "Author": "Lê Quang", "Year": 2022, "Publisher": "Lucy"},
        ]

        # Kết nối các sự kiện của nút bấm
        self.pushButtonSave.clicked.connect(self.save_book)
        self.pushButtonRemove.clicked.connect(self.remove_book)
        self.pushButtonSearchTitile.clicked.connect(self.search_book_by_title)
        self.pushButtonSearchISBN.clicked.connect(self.search_book_by_isbn)
        self.pushButtonFiltersYears.clicked.connect(self.filter_books_by_year)
        self.pushButtonFiltersPublisher.clicked.connect(self.filter_books_by_publisher)

        # Cập nhật danh sách sách
        self.update_book_list()

    def update_book_list(self):
        # Xóa tất cả các widget hiện có trong layout
        while self.verticalLayout.count():
            child = self.verticalLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Thêm lại các nút sách mới vào layout
        for book in self.books:
            button = QPushButton(f"ISBN: {book['ISBN']}, {book['Title']}, {book['Year']}, {book['Publisher']}")
            button.clicked.connect(lambda checked, b=book: self.display_book_details(b))
            self.verticalLayout.addWidget(button)

    def display_book_details(self, book):
        # Hiển thị thông tin chi tiết của một cuốn sách
        self.lineEditISBN.setText(book["ISBN"])
        self.lineEditTitile.setText(book["Title"])
        self.lineEditAuthor.setText(book["Author"])
        self.lineEditYear.setText(str(book["Year"]))
        self.lineEditPublisher.setText(book["Publisher"])

    def save_book(self):
        # Lưu hoặc cập nhật thông tin sách
        isbn = self.lineEditISBN.text()
        title = self.lineEditTitile.text()
        author = self.lineEditAuthor.text()
        year = int(self.lineEditYear.text())
        publisher = self.lineEditPublisher.text()

        # Kiểm tra nếu ISBN đã tồn tại
        for book in self.books:
            if book["ISBN"] == isbn:
                book["Title"] = title
                book["Author"] = author
                book["Year"] = year
                book["Publisher"] = publisher
                self.update_book_list()
                return

        # Thêm sách mới nếu ISBN chưa tồn tại
        self.books.append({"ISBN": isbn, "Title": title, "Author": author, "Year": year, "Publisher": publisher})
        self.update_book_list()

    def remove_book(self):
        # Xóa sách dựa trên ISBN
        isbn = self.lineEditISBN.text()
        self.books = [book for book in self.books if book["ISBN"] != isbn]
        self.update_book_list()

    def search_book_by_title(self):
        # Tìm sách theo tiêu đề
        title = self.lineEditTitile.text().lower()
        results = [book for book in self.books if title in book["Title"].lower()]
        self.display_search_results(results)

    def search_book_by_isbn(self):
        # Tìm sách theo ISBN
        isbn = self.lineEditISBN.text()
        results = [book for book in self.books if book["ISBN"] == isbn]
        self.display_search_results(results)

    def filter_books_by_year(self):
        # Lọc sách theo năm xuất bản
        year = int(self.lineEditYear.text())
        results = [book for book in self.books if book["Year"] == year]
        self.display_search_results(results)

    def filter_books_by_publisher(self):
        # Lọc sách theo nhà xuất bản
        publisher = self.lineEditPublisher.text().lower()
        results = [book for book in self.books if publisher in book["Publisher"].lower()]
        self.display_search_results(results)

    def display_search_results(self, results):
        # Hiển thị kết quả tìm kiếm trong danh sách sách
        while self.verticalLayout.count():
            child = self.verticalLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for book in results:
            button = QPushButton(f"ISBN: {book['ISBN']}, {book['Title']}, {book['Year']}, {book['Publisher']}")
            button.clicked.connect(lambda checked, b=book: self.display_book_details(b))
            self.verticalLayout.addWidget(button)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookManagementApp()
    window.show()
    sys.exit(app.exec())
