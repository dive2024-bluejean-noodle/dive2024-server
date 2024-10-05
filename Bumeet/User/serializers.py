from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password',
                  'local', 'id_photo', 'language', 'nationality', 'is_active',
                  'visa_number', 'age', 'sex', 'mento']
        extra_kwargs = {'password': {'write_only': True}}  # 비밀번호를 write-only로 설정

    def create(self, validated_data):
        # 사용자 생성 시 비밀번호 암호화
        user = CustomUser(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            local=validated_data['local'],
            id_photo=validated_data.get('id_photo'),
            language=validated_data.get('language', 'Korean'),
            nationality=validated_data.get('nationality', 'Korean'),
            sex=validated_data.get('sex', 'Male'),
            visa_number=validated_data['visa_number'],
            age=validated_data['age'],
            mento=validated_data['mento'],
            is_active=validated_data['is_active'],
        )
        user.set_password(validated_data['password'])  # 비밀번호 암호화
        user.save()
        return user

    def update(self, instance, validated_data):
        # 유저 인스턴스 업데이트
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.local = validated_data.get('local', instance.local)
        instance.id_photo = validated_data.get('id_photo', instance.id_photo)
        instance.language = validated_data.get('language', instance.language)
        instance.mento = validated_data.get('mento', instance.mento)

        # 멘토가 True이고 국적이 한국이 아닌 경우 예외 발생
        if instance.mento and instance.nationality != "Korea":
            raise serializers.ValidationError("멘토는 한국인만 가능합니다.")

        # 비밀번호가 있을 경우 암호화
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance

    def delete(self, instance):
        instance.is_active = False

        instance.save()
        return instance

