from django.views.generic import CreateView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from game.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user
from django.contrib import messages


class HomeView(TemplateView):
    template_name = 'home.html'


class CreateUserView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        valid = super(CreateUserView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid

class LobbyView(TemplateView):
    template_name = 'components/lobby/lobby.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LobbyView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LobbyView, self).get_context_data(**kwargs)
        games = Game()
        # get current open games to prepopulate the list

        # we're creating a list of games that contains just the id (for the link) and the creator
        available_games = [{'creator': game.creator.username, 'id': game.pk} for game in games.get_available_games()]
        # for the player's games, we're returning a list of games with the opponent and id
        player_games = games.get_games_for_player(self.request.user)

        return context

class GameView(TemplateView):
    template_name = 'components/game/game.html'
    game = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # get the game by the id
        self.game = Game.get_by_id(kwargs['game_id'])
        user = get_user(request)
        # check to see if the game is open and available for this user
        # if this player is the creator, just return
        if self.game.creator == user or self.game.opponent == user:
            return super(GameView, self).dispatch(request, *args, **kwargs)

        # if there is no opponent and the game is not yet completed,
        # set the opponent as this user
        if not self.game.opponent and not self.game.completed:
            self.game.opponent = user
            self.game.save()
            return super(GameView, self).dispatch(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, 'Sorry, the selected game is not available.')
            return redirect('/lobby/')

    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)
        context['game'] = self.game

        return context