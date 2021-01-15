#Bartek Konarzewski i Mateusz Konarzewski
#Klasyfikator na bazie support vector machine z biblioteki sklearn
#Klasyfikator zbóż - klasyfikuje ziarna zbóż do jednej z 3 odmian na podstawie powierzchni(Areał i parametru P)
#Klasyfikator Skóry - na podstawie informacji o kolorze fragmentu obrazu w formacie RGB ocenia czy
# wskazany fragment jest ludzką skórą czy nie
#Klasyfikator butelek - utworzony przez nas dataset z informacjami dotyczącymi 25 butelek po piwach różnych browarów
# klasyfikator na podstawie informacji o stosunku wysokości do średnicy w najszerzym punkcie (h/d) i wagi butelki
# klasyfikuje butelkę jaki zwrotna lub bezzwrotną
#odpalany z konsoli >python SVM_linear.py

# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

from sklearn import svm, datasets


class Classifier:
    '''
    inicjalizator klasy Classifier, przechowującej obiekty SVM.SVC klasyfikatora z biblioteki sklearn
    '''
    def __init__(self):
     self.svc_bottles = self.bottles_classifier()
     self.svc_seeds = self.seeds_classifier()
     self.svc_skin = self.skin_classifier()

    def seeds_classifier(self):
        '''
        Funkcja wczytuje dane ze zbioru danych, wywołuje metodę classify
        i informuje  o utworzeniu graficznego wykresu dla klasyfikatora

        :return: svc
        '''

        dataset = np.genfromtxt("seeds_dataset.txt", invalid_raise=False)
        svc = self.classify(dataset, 'linear', 50, "Areał", "Parametr P", "seeds.pdf")
        print("Utworzono graficzny wykres dla klasyfikatora zbóż pod nazwą seeds.pdf")
        return svc

    def bottles_classifier(self):
        '''
        Funkcja wczytuje dane ze zbioru danych, wywołuje metodę classify
        i informuje  o utworzeniu graficznego wykresu dla klasyfikatora
           :return: svc
           '''
        bottles = np.genfromtxt('bottles.txt', skip_header=1, usecols=(3, 4, 7))
        svc = self.classify(bottles, 'linear', 50, "Waga", "Wysokość/średnica", "bottles.pdf")
        print("Utworzono graficzny wykres dla klasyfikatora butelek pod nazwą bottles.pdf")
        return svc

    def skin_classifier(self):
        '''
        Funkcja wczytuje dane ze zbioru danych, wywołuje metodę classify
        i informuje  o utworzeniu graficznego wykresu dla klasyfikatora

        :return: svc
        '''
        skin = np.genfromtxt('Skin_NonSkin.txt', skip_header=50000, skip_footer=190000)
        svc = self.classify(skin, 'linear', 50, "Czerwony", "Zielony", "skin_graph.pdf")
        print("Utworzono graficzny wykres dla klasyfikatora skóry pod nazwą skin_graph.pdf")
        return svc

    def classify(self, dataset, kernel, gamma, xlabel, ylabel, output_file_name):
        '''
        Funkcja tworzy i zwraca obiekt svm.svc z biblioteki sklearn, pobiera dwie kolumny z datasetu
         i tworzy graficzny wykres klasyfikatora

        :param dataset:
        :param kernel:
        :param gamma:
        :param xlabel:
        :param ylabel:
        :param output_file_name:
        :return: svc
        '''
        seeds = dataset
        X = seeds[:, :2]
        target = []
        for i in seeds:
            target.append(i[-1])
        y = target
        svc = svm.SVC(kernel=kernel, C=1, gamma=gamma).fit(X, y)
        '''
         Tworzenie wykresu graficznego.
        '''
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        h = (x_max / x_min) / 100
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        plt.subplot(1, 1, 1)
        Z = svc.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)
        plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Paired)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xlim(xx.min(), xx.max())
        plt.title('SVC with linear kernel')
        plt.savefig(output_file_name)
        return svc

    def predict(self, classifier_no):
        '''
        Funkcja pobiera dane od użytkownika
        oraz drukuje wynik predykcji dla podanych danych.
        :param classifier_no:

        '''
        if classifier_no == '1':
            print("Podaj pierwszy atrybut dla klasyfikatora:")
            attr1 = input()
            print("Podaj drugi atrybut dla klasyfikatora:")
            attr2 = input()
            print("Według klasyfikatora to ", self.svc_seeds.predict([[attr1, attr2]]), " klasa ziarna")
        if classifier_no == '2':
            print("Podaj wartość koloru czerwonego")
            attr1 = input()
            print("Podaj wartość koloru zielongo")
            attr2 = input()
            result = self.svc_skin.predict([[attr1, attr2]])
            if(result == 1):
                print("Według klasyfikatora to jest skóra")
            if(result == 2):
                print("Według klasyfikatora to nie jest skóra")
        if classifier_no == '3':
            print("Podaj wysokość/średnica butelki")
            attr1 = input()
            print("Podaj wagę butelki w gramach")
            attr2 = input()
            result = self.svc_bottles.predict([[attr2, attr1]])
            if(result == 1):
                print("Według klasyfikatora to jest butelka wymienna")
            if(result == 0):
                print("Według klasyfikatora to nie jest butelka wymienna")


'''
Menu z wyborem klasyfikatora, którego chcemy użyć
'''
action = 'b'
classifier = Classifier()
print("Witaj w klasyfikatorze sklearn")

'''
pętla działania programu, program działa dopóki nie podamy 'q' na input
'''
while(action != 'q'):
    print("Z którego klasyfikatora chcesz skorzystać?")
    print("1 - Klasyfikator Zbóż")
    print("2 - Klasyfikator Skóry")
    print("3 - Klasyfikator Butelek")
    action = input()
    classifier.predict(action)