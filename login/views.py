from django.shortcuts import render , redirect
from django.views import View
from django.contrib.auth import authenticate , logout , login


class Login( View ):
	
	def get( self , request ):
		if request.user.is_authenticated:
			print("Usuario ya registrado uwu")
			return redirect( 'productos_troposfericos_vista' )
		return render( request , "login.html" )

	def post( self , request ):
		data_request = request.POST.dict()
		user = authenticate( username=data_request["username"] , password=data_request["password"] )
		if user is not None:
			login(request, user)
			print("Usuario ya registrado uwu 123123")
			return redirect( 'productos_troposfericos_vista' )
		else:
			return redirect( 'login_user' )


class Logout( View ):
	def get( self , request ):
		logout(request)
		return redirect( 'productos_troposfericos_vista' ) #Deslogueamos 