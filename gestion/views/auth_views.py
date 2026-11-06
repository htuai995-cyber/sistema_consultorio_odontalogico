from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from gestion.forms.auth_forms import LoginForm, RegistroForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    next_url = request.GET.get('next', 'dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if remember_me:
                    # 14 días de sesión activa
                    request.session.set_expiry(1209600)
                else:
                    # Expira al cerrar el navegador
                    request.session.set_expiry(0)

                messages.success(request, f'¡Bienvenido(a), {user.get_full_name() or user.username}!')
                return redirect(next_url if next_url else 'dashboard')
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {
        'form': form,
        'next': next_url,
    })


def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado la sesión correctamente.')
    return redirect('login')


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Cuenta creada exitosamente. Ya puede iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()

    return render(request, 'registration/registro.html', {
        'form': form,
    })

