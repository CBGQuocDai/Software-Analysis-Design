from django.core.management.base import BaseCommand
from core.dao.book_dao import BookDAO
from core.dao.customer_dao import CustomerDAO
from core.models.book import Book


class Command(BaseCommand):
    help = 'Load sample data for testing'

    def handle(self, *args, **options):
        # Check if data already exists
        if Book.objects.exists():
            self.stdout.write(self.style.WARNING('Dữ liệu mẫu đã tồn tại, bỏ qua'))
            return

        # Create sample books
        books_data = [
            {
                'title': 'Python Pro',
                'author': 'Nguyễn Văn A',
                'price': 150000,
                'stock': 10
            },
            {
                'title': 'Django Mastery',
                'author': 'Trần Thị B',
                'price': 180000,
                'stock': 8
            },
            {
                'title': 'Web Development Basics',
                'author': 'Lê Văn C',
                'price': 120000,
                'stock': 15
            },
            {
                'title': 'Database Design',
                'author': 'Phạm Thị D',
                'price': 160000,
                'stock': 12
            },
            {
                'title': 'REST API Guide',
                'author': 'Đỗ Văn E',
                'price': 140000,
                'stock': 20
            },
            {
                'title': 'Vue.js Complete Guide',
                'author': 'Vũ Thị F',
                'price': 175000,
                'stock': 9
            },
        ]

        for book_data in books_data:
            book = BookDAO.create_book(**book_data)
            self.stdout.write(self.style.SUCCESS(f'Đã tạo sách: {book.title}'))

        self.stdout.write(self.style.SUCCESS('Dữ liệu mẫu đã được tải'))
