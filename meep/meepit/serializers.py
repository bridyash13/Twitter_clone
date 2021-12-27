from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from rest_framework.response import Response
from .models import Follower, UserModel, Meep
from django.utils.timezone import now


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = '__all__'
        extra_kwargs = {'username': {'required': False}}

    def save(self):
        user = UserModel(name=self.validated_data['name'],
                         email=self.validated_data['email'],
                         uname=self.validated_data['uname'], 
                         bio = self.validated_data['bio'],
                         username = self.validated_data['uname']
                         )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match'})
        user.set_password(password)
        user.save()
        return user


class MeepSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meep
        fields = '__all__'
        
    def save(self):
        text = self.validated_data['meeptext']
        userid = self.context['userid']
        user = UserModel.objects.get(id=userid)
        if len(text)>200:
            raise serializers.ValidationError(
                {'text': 'Meep length exceeds limit'})
        meep = Meep(meeptext = text,userid=user)
        meep.save()
        return meep


class FollowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follower
        fields = '__all__'

    def save(self):
        followerobj = UserModel.objects.get(id=self.context['userid'])
        falready = Follower.objects.filter(follower = followerobj,person = self.context['person'])
        if followerobj.uname == self.context['person']:
            raise serializers.ValidationError(
                {'FollowError': 'You cannot follow yourself'})
        if not falready:
            follower = Follower(follower = followerobj, person = self.context['person'])
            follower.save()
            return follower
        else:
            raise serializers.ValidationError(
                {'FollowError': 'You already follow this person'})


class MeepFeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follower
        fields = '__all__'

    def save(self):
        userid = self.context['userid']
        user = UserModel.objects.get(id=userid)
        people = list(Follower.objects.filter(follower=user))
        if len(people)>0:
            person = []
            for i in people:
                person.append(str(i.person))
            print(person)
            personlist = list(UserModel.objects.filter(uname__in=person))
            meeps = list(Meep.objects.filter(userid__in=personlist))
            if len(meeps)>0:
                meeps.sort(key=lambda x: x.meepid, reverse=True)
                return meeps
            else:
                raise serializers.ValidationError(
                {'Meep Error': 'No one has meeped anything'})
        else:
            raise serializers.ValidationError(
                {'People Error': 'You do no follow anyone'})

