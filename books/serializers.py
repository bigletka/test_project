from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Author, Book, Favourite, Genre, Review

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = ['author', 'rating', 'text']


class BookListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genre = GenreSerializer()
    is_favourite = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'average_rating',
                  'is_favourite']

    def get_average_rating(self, obj) -> int:
        average = obj.average_rating
        return int(average) if average is not None else 0

    def get_is_favourite(self, obj) -> bool:
        request = self.context.get('request', None)
        if request is None or request.user.is_anonymous:
            return False
        return Favourite.objects.filter(user=request.user, book=obj).exists()


class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genre = GenreSerializer()
    is_favourite = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'average_rating',
                  'is_favourite', 'description', 'publication_date', 'reviews']

    def get_is_favourite(self, obj) -> bool:
        request = self.context.get('request', None)
        if request is None or request.user.is_anonymous:
            return False
        return Favourite.objects.filter(user=request.user, book=obj).exists()

    def get_average_rating(self, obj) -> int:
        average = obj.average_rating
        return int(average) if average is not None else 0


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'


class ReviewPerformSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ['book', 'author', 'rating', 'text']

    def validate(self, data):
        if not 1 <= data['rating'] <= 5:
            raise serializers.ValidationError("Rating must be \
                                              between 1 and 5.")
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']
        ref_name = 'CustomUserSerializer'


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password',
                  'password2']
        ref_name = 'CustomUserCreateSerializer'

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields \
                                               didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
