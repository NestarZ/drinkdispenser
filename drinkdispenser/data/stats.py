#!/bin/python3
# -*- coding: utf-8 -*-


class Stats(object):

    def __init__(self, ingredients, boissons):
        self.boissons = boissons.values()
        self.ingredients = ingredients.values()
        self.nb_vendu = {boisson.nom: 0 for boisson in self.boissons}
        self.dose_sucre = {boisson.nom: [] for boisson in self.boissons}
        self.with_lait = {boisson.nom: 0 for boisson in self.boissons}
        self.conso_ingredient = {
            ingredient.nom: 0 for ingredient in self.ingredients}

    @property
    def mean_sucre(self):
        return {
            boisson: int(
                sum(l) /
                float(
                    len(l))) if len(l) > 0 else 0 for boisson,
            l in self.dose_sucre.items()}

    @property
    def prop_vendu(self):
        return {
            boisson: int(
                100 *
                self.nb_vendu[boisson] /
                sum(
                    self.nb_vendu.values())) if sum(
                self.nb_vendu.values()) > 0 else 0 for boisson in self.nb_vendu}

    @property
    def prop_with_sucre(self):
        return {
            boisson: int(
                100 *
                sum(
                    x > 0 for x in self.dose_sucre[boisson]) /
                self.nb_vendu[boisson]) if self.nb_vendu[boisson] > 0 else 0 for boisson in self.dose_sucre}

    @property
    def prop_with_lait(self):
        return {
            boisson: int(
                100 *
                self.with_lait[boisson] /
                self.nb_vendu[boisson]) if self.nb_vendu[boisson] > 0 else 0 for boisson in self.with_lait}

    @property
    def prop_conso(self):
        return {
            ing.nom: int(
                100 *
                self.conso_ingredient[ing.nom] /
                sum(
                    self.conso_ingredient.values())) if sum(
                self.conso_ingredient.values()) > 0 else 0 for ing in self.ingredients}

    def display_all(self):
        stats1 = {"Vendu": self.nb_vendu,
                 "Moy. Sucre": self.mean_sucre,
                 "+Lait%": self.prop_with_lait,
                 "+Sucre%": self.prop_with_sucre,
                 "Vendu%": self.prop_vendu}
        str_stat1 = self.display(self.boissons, stats1)

        stats2 = {"#Conso": self.conso_ingredient,
                 "%Conso": self.prop_conso}
        str_stat2 = self.display(self.ingredients, stats2)

        print(str_stat1 + str_stat2)

    def display(self, items, stats):
        txt_a = a = ""
        txt_b = txt_c = []
        spaces = max([len(str(boisson))
                      for boisson in list(items) + list(stats.keys())]) + 1
        txt_a = " " * spaces
        for boisson in items:
            txt_a += "{}{}".format(str(boisson), " " *
                                   (spaces - len(str(boisson))))
            txt_b = []
            for stat in stats.values():
                txt_b.append(str(stat[boisson.nom]))
            txt_c.append(txt_b)
        a += txt_a + "\n"
        for i in range(len(stats)):
            a += "{}{}".format(list(stats.keys())
                               [i], " " * (spaces - len(list(stats.keys())[i])))
            for x in txt_c:
                a += "{}{}".format(x[i], " " * (spaces - len(x[i])))
            a += "\n"
        return a
