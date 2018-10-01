from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=20, verbose_name='카테고리명',)

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


class Restaurant(models.Model):
    name = models.CharField(max_length=20, verbose_name='음식점 이름',)
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE, verbose_name='카테고리',)
    # main_image = models.ImageField(blank=True, verbose_name='음식점 사진',)
    menu = models.ForeignKey(Menu, blank=True, on_delete=models.CASCADE, verbose_name='음식점 메뉴',)
    open_to_close = models.TextField(blank=True, verbose_name='오픈 & 마감',)
    STATUS_CHOICES = (
        ('가능', '가능'),
        ('불가능', '불가능'),
    )
    is_package_possible = models.TextField(blank=True, choices=STATUS_CHOICES, verbose_name='포장 가능 여부', )
    is_delivery_possible = models.TextField(blank=True, choices=STATUS_CHOICES, verbose_name='배달 가능 여부', )
    is_eating_lonely_possible = models.TextField(blank=True, choices=STATUS_CHOICES, verbose_name='혼밥 가능 여부', )
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
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='작성자')   # Profile의 user와 같은 거?? 따로 부름??
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='해당 가게')

    # 구글 평점 가져오기
    # 모델 class 하나 더 파서 하는 좋은 방법 없나 생각!
    price_star = models.IntegerField(verbose_name='가격 만족도',)
    taste_star = models.IntegerField(verbose_name='맛 만족도',)
    clean_star = models.IntegerField(verbose_name='청결성 만족도',)

    # 위에 것으로 자동 계산할 듯함
    # avg_star = models.IntegerField(verbose_name='평점(평균 점수)',)


    # 먹은 음식의 종류랑 평점 연결이 자유롭게 어떻게..!?
    # dish_eaten = models.CharField(max_length=20, verbose_name='먹은 음식',)
    dish_eaten = models.ForeignKey(Menu, blank=True, on_delete=models.CASCADE, verbose_name='먹은 음식',)

    content = models.CharField(max_length=20, verbose_name='20자평',)

    STATUS_CHOICES = (
        ('꼭 다시 먹는다', '꼭 다시 먹는다'),
        ('잘 모르겠다', '잘 모르겠다'),
        ('절대 안 먹는다', '절대 안 먹는다'),
    )
    try_again = models.TextField(choices=STATUS_CHOICES, verbose_name='다시 먹을 지 여부',)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    # comment 쓰고 다시 그 페이지로(그대로 따옴, 수정 필요)
    # def get_absolute_url(self):
    #     return reverse('main_app:product', args=[self.product.id])
