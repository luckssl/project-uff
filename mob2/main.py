# -*- coding: utf-8 -*-

import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
import webbrowser

with open('dados.txt', 'r', encoding='utf-8') as arquivo:
    dados = json.load(arquivo)
    tur_permitidos = []
    cod_permitidos = list(dados["cod_permitidos"].keys())
    for i in dados["cod_permitidos"].keys():
        tur_permitidos.extend(list(dados["cod_permitidos"][i]["tur_permitidos"].keys()))

class TelaInicial(Screen):
    def release(self,codigo_entry,turma_entry):
        cod = codigo_entry.text
        tur = turma_entry.text
        codigo_entry.text = ''
        turma_entry.text = ''
        if cod == '' or tur == '':
            self.ids.error.text ='Preencha todos os campos!'
        elif cod not in cod_permitidos or tur not in tur_permitidos:
            self.ids.error.text = "Código ou turma não cadastrados no sistema."
        else:
            self.ids.error.text =''
            for i in cod_permitidos:
                if cod == i:
                    mat = dados["cod_permitidos"][i]["mat"]
                    inst = dados["cod_permitidos"][i]["inst"]
                    local = dados["cod_permitidos"][i]["local"]
                    codigo_confirmado = i
                    break
            for j in tur_permitidos:
                if tur == j:
                    dsem = dados["cod_permitidos"][codigo_confirmado]["tur_permitidos"][j]["dsem"]
                    sala = dados["cod_permitidos"][codigo_confirmado]["tur_permitidos"][j]["sala"]
                    hor = dados["cod_permitidos"][codigo_confirmado]["tur_permitidos"][j]["hor"]
                    tur_confirmado = j
                    break

            infor="informacoes"
            if inst=='Bloco H':
                infor='informacoes2'
                
            self.manager.get_screen(infor).dados_disciplinas = {
                "mat":mat,
                "tur":tur_confirmado,
                "inst":inst,
                "local":local,
                "dsem":dsem,
                "sala":sala,
                "hor":hor
            }
            self.manager.current = infor

            


class TelaInformacoes(Screen):
    def on_enter(self):
        informacoes = self.manager.get_screen("informacoes").dados_disciplinas
        self.ids.materia.text = f"Disciplina: {informacoes['mat']}"
        self.ids.turma.text = f"Sua turma é a {informacoes['tur']}"
        self.ids.instituto.text = f"No {informacoes['inst']}"
        self.ids.hora.text =  f"Sua aula será às {informacoes['dsem']} das {informacoes['hor']} na sala {informacoes['sala']}"



    def retorno(self):
        self.manager.current = "inicial"

    def localizar(self):
        informacoes = self.manager.get_screen("informacoes").dados_disciplinas
        webbrowser.open(informacoes["local"])


class TelaInformacoes2(Screen):
    def on_enter(self):
        informacoes = self.manager.get_screen("informacoes2").dados_disciplinas
        self.ids.materia.text = f"Disciplina: {informacoes['mat']}"
        self.ids.turma.text = f"Sua turma é a {informacoes['tur']}"
        self.ids.instituto.text = f"No {informacoes['inst']}"
        self.ids.hora.text =  f"Sua aula será às {informacoes['dsem']} das {informacoes['hor']} na sala {informacoes['sala']}"

    def retorno(self):
        self.manager.current = "inicial"

    def localizar(self):
        informacoes = self.manager.get_screen("informacoes2").dados_disciplinas
        webbrowser.open(informacoes["local"])
class Telas(ScreenManager):
    pass

kv = Builder.load_file('localizauff.kv')



class LocalizaUFF(App):
    def build(self):
        return kv

if __name__ ==  '__main__':
    LocalizaUFF().run()