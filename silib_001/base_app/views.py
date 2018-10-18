from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant, Category, Comment
from django.db.models import Q, Avg


# Create your views here.
def base(request):
    restaurants = Restaurant.objects.all()
    categorys = Category.objects.all()

    # 카테고리 별 restaurants 추출
    category_restaurants = {}
    for category in categorys:
        category_restaurants[category] = Restaurant.objects.filter(category=category)

    # comment 에 있는 average_star 다 더해서 전체 평점 구하기
    # 숫자로 받은 값을 grade 시스템으로
    def number_to_grade(self):
        if self > 4:
            grade = 'A+'
        elif self >= 3.5:
            grade = 'A'
        elif self > 3:
            grade = 'B+'
        elif self >= 2.5:
            grade = 'B'
        elif self > 2:
            grade = 'C+'
        elif self >= 1.5:
            grade = 'C'
        elif self > 1:
            grade = 'D+'
        elif self >= 0.5:
            grade = 'D'
        else:
            grade = 'F'
        return grade
    for restaurant in restaurants:
        restaurant.comment_count = "(" + str(restaurant.comment_set.all().count()) + ")"
        if restaurant.comment_set.all().aggregate(Avg('taste_star'))['taste_star__avg'] is None:
            restaurant.average_star = "-"
        else:
            taste_star = restaurant.comment_set.all().aggregate(Avg('taste_star'))['taste_star__avg']
            price_star = restaurant.comment_set.all().aggregate(Avg('price_star'))['price_star__avg']
            clean_star = restaurant.comment_set.all().aggregate(Avg('clean_star'))['clean_star__avg']
            restaurant.taste_star = number_to_grade(taste_star)
            restaurant.price_star = number_to_grade(price_star)
            restaurant.clean_star = number_to_grade(clean_star)
            restaurant.average_number = taste_star + price_star + clean_star
            restaurant.average_star = number_to_grade(taste_star + price_star + clean_star)
        restaurant.save()

    # TODO: 필터별 restaurants 분류
    # restaurants.sort_grade = sorted(restaurants, key=lambda x: x.average_number, reverse=True)
    # restaurants.sort_comments =
    # restaurants.save()

    ctx = {
        'restaurants': restaurants,
        'categorys': categorys,
        'category_restaurants': category_restaurants,
    }
    return render(request, 'base_app/base.html', ctx)

# def category(request, pk):
#     category = Category.objects.filter(pk=pk)
#     restaurants = Restaurant.objects.filter(category__pk=pk)
#     ctx = {
#         'restaurants': restaurants,
#         'category': category,
#     }
#     return render(request, 'base_app/category.html', ctx)


def restaurant(request, pk):
    restaurants = Restaurant.objects.all()
    selected_restaurant = Restaurant.objects.filter(pk=pk)
    comments = Comment.objects.filter(restaurant__pk=pk)

    # 숫자로 받은 값을 grade 시스템으로
    def number_to_grade(self):
        if self > 4:
            grade = 'A+'
        elif self >= 3.5:
            grade = 'A'
        elif self > 3:
            grade = 'B+'
        elif self >= 2.5:
            grade = 'B'
        elif self > 2:
            grade = 'C+'
        elif self >= 1.5:
            grade = 'C'
        elif self > 1:
            grade = 'D+'
        elif self >= 0.5:
            grade = 'D'
        else:
            grade = 'F'
        return grade
    for comment in comments:
        comment.taste_grade = number_to_grade(comment.taste_star)
        comment.price_grade = number_to_grade(comment.price_star)
        comment.clean_grade = number_to_grade(comment.clean_star)
        comment.average_grade = number_to_grade(comment.average_star())
        comment.save()

    # comment 에 있는 average_star 다 더해서 전체 평점 구하기
    for restaurant in restaurants:
        if restaurant.comment_set.all().aggregate(Avg('taste_star'))['taste_star__avg'] is None:
            restaurant.average_star = "-"
        else:
            taste_star = restaurant.comment_set.all().aggregate(Avg('taste_star'))['taste_star__avg']
            price_star = restaurant.comment_set.all().aggregate(Avg('price_star'))['price_star__avg']
            clean_star = restaurant.comment_set.all().aggregate(Avg('clean_star'))['clean_star__avg']
            restaurant.average_star = number_to_grade(taste_star + price_star + clean_star)
        restaurant.save()
    for restaurant in selected_restaurant:
        if restaurant.comment_set.all().aggregate(Avg('taste_star'))['taste_star__avg'] is None:
            restaurant.average_star = "-"
        else:
            taste_star = restaurant.comment_set.all().aggregate(Avg('taste_star'))['taste_star__avg']
            price_star = restaurant.comment_set.all().aggregate(Avg('price_star'))['price_star__avg']
            clean_star = restaurant.comment_set.all().aggregate(Avg('clean_star'))['clean_star__avg']
            restaurant.taste_star = number_to_grade(taste_star)
            restaurant.price_star = number_to_grade(price_star)
            restaurant.clean_star = number_to_grade(clean_star)
            restaurant.average_star = number_to_grade(taste_star + price_star + clean_star)
        restaurant.save()

    ctx = {
        'restaurants': restaurants,
        'selected_restaurant': selected_restaurant,
        'comments': comments,
    }
    return render(request, 'base_app/restaurant.html', ctx)
