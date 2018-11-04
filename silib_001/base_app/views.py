from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant, Category, Comment
from django.db.models import Q, Avg


# Create your views here.
def base(request):
    # filter 구현
    if "category" in request.GET:
        sort_term = request.GET["sort"]
        category = request.GET["category"]
        category = category.split(',')
        category_term = []
        for a in category:
            b = a.splitlines()[0]
            category_term.append(b)

        restaurants = Restaurant.objects.filter(category__category_name__in=category_term)
        categorys = Category.objects.all()
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
                restaurant.average_star = number_to_grade(taste_star + price_star + clean_star)
            restaurant.save()

        # 필터별 restaurants 분류
        def sum_none(a, b, c):
            if a is None:
                a = 0
                b = 0
                c = 0
            return a + b + c
        def comment_star(x, y):
            return x.comment_set.all().aggregate(Avg(y))[y + '__avg']

        # sort로 분류
        if sort_term == "평점순":
            restaurants = sorted(restaurants,
                                key=lambda x: sum_none(comment_star(x, 'taste_star'), comment_star(x, 'price_star'),
                                                       comment_star(x, 'clean_star'))
                                , reverse=True)
        elif sort_term == "인기순":
            restaurants = sorted(restaurants, key=lambda x: x.comment_set.count(), reverse=True)
        else:
            restaurants = restaurants

        # restaurant numbering
        i = 1
        for restaurant in restaurants:
            restaurant.number = i
            i += 1
            restaurant.save()

        ctx = {
            'categorys': categorys,
            'restaurants': restaurants,
        }
        return render(request, 'base_app/base.html', ctx)

    # search 구현
    if "search" in request.GET:
        search_term = request.GET["search"]
        if search_term:
            searched_restaurants = Restaurant.objects.filter(
                Q(name__icontains=search_term) |
                Q(menu__category__icontains=search_term) |
                Q(menu__name__icontains=search_term) |
                Q(category__category_name__icontains=search_term) |
                Q(detail__icontains=search_term)
            ).distinct()

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
        for restaurant in searched_restaurants:
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
                restaurant.average_star = number_to_grade(taste_star + price_star + clean_star)
            restaurant.save()

        # 필터별 restaurants 분류
        def sum_none(a,b,c):
            if a is None:
                a = 0
                b = 0
                c = 0
            return a + b + c
        def comment_star(x, y):
            return x.comment_set.all().aggregate(Avg(y))[y + '__avg']

        sort_grade = sorted(searched_restaurants,
                            key=lambda x: sum_none(comment_star(x, 'taste_star'), comment_star(x,'price_star'), comment_star(x,'clean_star'))
                            , reverse=True)
        categorys = Category.objects.all()

        # restaurant numbering
        i = 1
        for restaurant in sort_grade:
            restaurant.number = i
            i += 1
            restaurant.save()
        
        ctx = {
            'search_term': search_term,
            'restaurants': sort_grade,
            'categorys': categorys,
        }
        return render(request, 'base_app/search_restaurant.html', ctx)

    restaurants = Restaurant.objects.all()
    categorys = Category.objects.all()

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
            restaurant.average_star = number_to_grade(taste_star + price_star + clean_star)
        restaurant.save()

    # 필터별 restaurants 분류
    def sum_none(a,b,c):
        if a is None:
            a = 0
            b = 0
            c = 0
        return a + b + c
    def comment_star(x, y):
        return x.comment_set.all().aggregate(Avg(y))[y + '__avg']

    sort_grade = sorted(restaurants,
                        key=lambda x: sum_none(comment_star(x, 'taste_star'), comment_star(x,'price_star'), comment_star(x,'clean_star'))
                        , reverse=True)

    # restaurant numbering
    i = 1
    for restaurant in sort_grade:
        restaurant.number = i
        i += 1
        restaurant.save()

    ctx = {
        'categorys': categorys,
        'restaurants': sort_grade,
    }
    return render(request, 'base_app/base.html', ctx)


def restaurant(request, pk):
    restaurants = Restaurant.objects.all()
    categorys = Category.objects.all()
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
        'categorys': categorys,
        'selected_restaurant': selected_restaurant,
        'comments': comments,
    }
    return render(request, 'base_app/restaurant.html', ctx)


def all_comments(request):
    # search 구현
    if "search" in request.GET:
        search_term = request.GET["search"]
        if search_term:
            searched_comments = Comment.objects.filter(
                Q(dish_eaten__name__icontains=search_term) |
                Q(dish_eaten__category__icontains=search_term) |
                Q(restaurant__name__icontains=search_term) |
                Q(content__icontains=search_term)
            ).distinct()
            restaurants = Restaurant.objects.all()
            categorys = Category.objects.all()

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
            for comment in searched_comments:
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

            ctx = {
                'restaurants': restaurants,
                'categorys': categorys,
                'search_term': search_term,
                'comments': searched_comments,
            }
            return render(request, 'base_app/search_comments.html', ctx)
    restaurants = Restaurant.objects.all()
    categorys = Category.objects.all()
    comments = Comment.objects.all()

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

    ctx = {
        'restaurants': restaurants,
        'categorys': categorys,
        'comments': comments,
    }
    return render(request, 'base_app/all_comments.html', ctx)


def write_comment(request, pk):
    restaurants = Restaurant.objects.all()
    categorys = Category.objects.all()
    restaurant = Restaurant.objects.filter(pk=pk).first()

    ctx = {
        'restaurants': restaurants,
        'categorys': categorys,
        'selected_restaurant': restaurant,
    }
    return render(request, 'base_app/write_comment.html', ctx)
