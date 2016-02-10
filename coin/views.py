__author__ = 'kolobok'

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from coin.models import Section, Coin, Metal, Edge
from coin.form import CoinForm


def main(request):
    if not request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        section_list = Section.objects.all()
        return render(request, 'index.html', {'section_list': section_list})
    return render(request, 'index.html')


def sections(request):
    return render(request, 'index.html')


def coins_section(request, id_section):
    coins = Coin.objects.filter(section=id_section)
    section = Section.objects.get(pk=id_section)
    return render_to_response('section.html', {'section': section, 'coins': coins}, context_instance=RequestContext(request))


def information_coin(request, id_coin):
    coin = Coin.objects.get(pk=id_coin)

    metal_list = []
    for metal in coin.metal.all():
        metal_list.append(metal.name)
    edge = Edge.objects.filter(coin__id=coin.id)
    coin_form = CoinForm(instance=coin, initial={'edge': edge.first().name, 'metal': ','.join(metal_list)}, label_suffix='')
    return render_to_response('coin.html', {'coin': coin, 'coin_form': coin_form}, context_instance=RequestContext(request))