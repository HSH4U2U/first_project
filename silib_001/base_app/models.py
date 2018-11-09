from django.db import models
from django.conf import settings
from django.urls import reverse
from imagekit.processors import Thumbnail
from imagekit.models import ProcessedImageField


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=20, verbose_name='카테고리명',)
    category_image = models.ImageField(blank=True, verbose_name='카테고리 사진',)

    def __str__(self):
        return self.category_name


class Menu(models.Model):
    category = models.CharField(max_length=20, verbose_name='음식 종류(밥, 국, 주류...)',)
    name = models.CharField(max_length=20, verbose_name='음식명',)
    price = models.IntegerField(verbose_name='음식 가격',)

    # 아마 이 평점이 나중에 각 음식별 평점으로 쓰일 듯
    # dish_star = models.IntegerField(verbose_name='음식 평점',)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=12, verbose_name='음식점 이름',)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE, verbose_name='카테고리',)
    # main_image = models.ImageField(blank=True, verbose_name='음식점 사진',)
    phone_number = models.CharField(blank=True, max_length=17, verbose_name='음식점 전화번호',)
    menu = models.ForeignKey(Menu, null=True, blank=True, on_delete=models.CASCADE, verbose_name='음식점 메뉴',)
    open_to_close = models.TextField(blank=True, verbose_name='오픈 & 마감',)
    STATUS_CHOICES = (
        ('O', 'O'),
        ('X', 'X'),
        ('-', '-'),
    )
    is_package_possible = models.TextField(blank=True, choices=STATUS_CHOICES, verbose_name='포장 가능 여부', )
    is_delivery_possible = models.TextField(blank=True, choices=STATUS_CHOICES, verbose_name='배달 가능 여부', )
    is_card_possible = models.TextField(blank=True, choices=STATUS_CHOICES, verbose_name='카드 가능 여부', )
    detail = models.TextField(blank=True, verbose_name='음식점 설명',)
    latitude = models.CharField(max_length=20,)
    longitude = models.CharField(max_length=20,)
    register = models.DateTimeField(auto_now_add=True, verbose_name='음식점 등록일',)

    # 경도, 위도로 장소 자동추가
    def locate(self):
        locate = "{lat:" + self.latitude + ", lng:" + self.longitude + "}"
        return locate

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='작성자', null=True,)   # Profile의 user와 같은 거?? 따로 부름??
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='해당 가게')

    # TODO: 구글 평점 가져오기
    STATUS_CHOICES = (
        (4, 'A'),
        (3, 'B'),
        (2, 'C'),
        (1, 'D'),
        (0, 'F'),
    )
    price_star = models.IntegerField(verbose_name='가격 만족도',)
    taste_star = models.IntegerField(verbose_name='맛 만족도',)
    clean_star = models.IntegerField(verbose_name='청결성 만족도',)
    dish_eaten = models.CharField(max_length=30, blank=True, null=True, verbose_name='먹은 음식',)
    content = models.CharField(max_length=160, verbose_name='150자평', blank=True, null=True,)
    food_image = ProcessedImageField(
        upload_to="blog/%Y/%m/%d", blank=True, null=True,
        # processors=[Thumbnail(500, 500)],  # 처리할 작업 목룍
        format='JPEG',  # 최종 저장 포맷
        options={'quality': 70}  # 저장 옵션
    )
    STATUS_CHOICES = (
        ('꼭 다시 먹는다', '꼭 다시 먹는다'),
        ('잘 모르겠다', '잘 모르겠다'),
        ('절대 안 먹는다', '절대 안 먹는다'),
    )
    try_again = models.TextField(choices=STATUS_CHOICES, verbose_name='다시 먹을 지 여부', null=True, blank=True,)
    # police = models.IntegerField(verbose_name='신고 수',)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def average_star(self):
        average_star = self.taste_star / 2 + self.price_star / 4 + self.clean_star / 4
        return average_star

    # comment 쓰고 다시 그 페이지로(그대로 따옴, 수정 필요)
    # def get_absolute_url(self):
    #     return reverse('main_app:product', args=[self.product.id])
