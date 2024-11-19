from rest_framework import serializers
from movie_app.models import Director, Movie, Review
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ConfirmationCode

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, is_active=False)
        code = ConfirmationCode.objects.create(user=user, code=ConfirmationCode.generate_code())
        # Здесь можно отправить код пользователю по email или SMS
        print(f"Confirmation code: {code.code}")
        return user


class ConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        username = attrs.get('username')
        code = attrs.get('code')
        try:
            user = User.objects.get(username=username)
            if user.confirmation_code.code != code:
                raise serializers.ValidationError("Invalid confirmation code.")
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")
        return attrs

    def save(self, **kwargs):
        username = self.validated_data.get('username')
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        user.confirmation_code.delete()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        if not user.is_active:
            raise serializers.ValidationError("User is not confirmed.")
        return user


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Имя директора должно быть длиной не менее 2 символов.")
        return value

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Название фильма должно быть длиной не менее 2 символов.")
        return value

    def validate_year(self, value):
        if value < 1888:
            raise serializers.ValidationError("Год выпуска фильма должен быть больше 1888.")
        return value

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_text(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Текст отзыва должен содержать не менее 10 символов.")
        return value

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Рейтинг должен быть в диапазоне от 1 до 5.")
        return value