from mysql.connector import Error
import function
import objects

try:
    connection = function.connect()  # Uzyskiwanie łączności z bazą danych

    if connection.is_connected():  # Sprawdzanie czy istnieje łączność
        db_info = connection.get_server_info()
        print("Połączono z serwerem MySQL. Wersja:", db_info)
        print("Witamy w Bazie Danych 'Fryzjerzy'!")

        end_program = False

        while not end_program:
            print(f"\n"
                  f"Wybierz jedną z dostępnych opcji:\n"
                  f"1 - Logowanie\n"
                  f"2 - Rejestracja\n"
                  f"3 - Wyszukiwanie salonu\n"
                  f"4 - Wyjście z programu\n")

            user_choice = int(input("Wybierz jedną z dostepnych opcji, wciskając odpowiednią liczbę: "))

            if user_choice == 1:
                email = input("\nAby się zalogować, proszę podać swój adres e-mail: ")
                password = input("Proszę podać hasło: ")

                if function.check_email_password(email, password, connection):

                    dane = function.fetch_user_data(email, connection)
                    User = objects.User(*dane)

                    logged_in = True

                    while logged_in:
                        if not User.Moderator and not User.Administrator: # zwykły użytkownik

                            action = function.user_action(User, connection)

                            if action == 'logout':
                                logged_in = False
                                del User

                        elif User.Administrator:  # Zakładam, że masz pole administrator w klasie User
                            print("\nJesteś administratorem.")
                            print("1: Dodaj salon")
                            print("2: Dodaj usługę")
                            print("3. Przeglądaj opinie")
                            print("4. Przegladaj raporty")
                            print("5: Wyloguj sie")
                            print("6: Wyjdz")
                            wybor = int(input("Wybierz opcję: "))
                            if wybor == 1:
                                function.dodaj_salon(connection)
                            elif wybor == 2:
                                function.zarzadzaj_uslugami(connection, User)
                            elif wybor == 3:
                                function.przeglądaj_opinie(connection)
                            elif wybor == 4:
                                function.przeglądaj_raporty(connection)
                            elif wybor == 5:
                                logged_in = False
                                del User
                            elif wybor == 6:
                                exit()

                        elif User.Moderator:
                            print("\nJesteś moderatorem.\n")
                            print("1: Zaktualizuj dane salonu")
                            print("2. Zarzadzaj uslugami salonu")
                            print("3: Wyloguj się")
                            print("4: Wyjdz")
                            print("5: Zarządzaj pracownikami salonu")
                            print("6: Zarzadzaj godzinami otwarcia salonu")
                            print("7: Zarzadzaj cenami uslug")
                            print("8. Zarządzaj czasem usług")
                            print("9: Dodaj raport\n")

                            wybor = input("Wybierz opcję: ")
                            if wybor == "1":
                                function.aktualizuj_salon(connection, User)
                            elif wybor == "2":
                                function.zarzadzaj_uslugami_salonu(connection, User)
                            elif wybor == "3":
                                logged_in = False
                                del User
                            elif wybor == "4":
                                exit()
                            elif wybor== "5":
                                User.zarzadzaj_pracownikami(connection)
                            elif wybor == "6":
                                User.zarzadzaj_godzinami_otwarcia(connection)
                            elif wybor == "7":
                                # Tutaj wywołanie funkcji ustaw_cene_uslugi
                                while True:
                                    print("1: Ustaw/zmien cene dla wybranej uslugi")
                                    print("2: Wyswietl ceny uslug")
                                    #print("3: Zmien ceny wszystkich uslug")
                                    print("3: Przejsc do poprzedniego ekranu")
                                    ch = int(input("Co chcesz zrobic? "))
                                    if ch == 1:
                                        print("Ceny podawaj z '.', a nie z ','!!!")
                                        function.wyswietl_ceny_uslug(connection,User.Moderator)
                                        service_id = input("Podaj ID usługi: ")
                                        cena = input("Podaj cenę dla tej usługi: ")
                                        function.ustaw_cene_uslugi(connection, User, service_id, cena)
                                    elif ch == 2:
                                        function.wyswietl_ceny_uslug(connection,User.Moderator)
                                    #elif ch == 3:
                                     #   print("Ceny podawaj z '.', a nie z ','!!!")
                                      #  function.aktualizuj_ceny_uslug(connection,User)
                                    elif ch == 3:
                                        break
                            elif wybor == "8":
                                while True:
                                    print("1. Ustaw/zmień czas dla wybranej uslugi")
                                    print("2. Wyswietl czasy wykonywania uslug")
                                    print("3. Przejsc do poprzedniego ekranu")
                                    ch = int(input("Co chcesz zrobić? "))
                                    # print("\n")
                                    if ch == 1:
                                        # print("Ceny podawaj z '.', a nie z ','!!!")
                                        function.wyswietl_czasy_uslug(connection, User.Moderator)
                                        service_id = input("Podaj ID usługi: ")
                                        czas = float(input("Podaj przyblizony czas dla uslugi: "))
                                        function.ustaw_czas_uslugi(connection, User, service_id, czas)
                                    elif ch == 2:
                                        function.wyswietl_czasy_uslug(connection,User.Moderator)
                                    elif ch == 3:
                                        break
                            elif wybor == "9":
                                function.add_report(User,connection)





                        else:
                            print(
                                "Nie masz uprawnień administratora ani moderatora jesteś zwykłym userem.")  # imo też tego nie powinno być
                            print("1: Wyloguj")
                            print("2: Wyjdź")
                            wybor = input("Wybierz opcję: ")
                            if wybor == "1":
                                logged_in = False
                                del User
                            elif wybor == "2":
                                exit()

            elif user_choice == 2:
                while True:
                    imie = input("Proszę podać imię: ")
                    if not imie.istitle():
                        print("Imię musi zaczynać się z wielkiej litery.")
                        continue
                    break

                while True:
                    nazwisko = input("Proszę podać nazwisko: ")
                    if not nazwisko.istitle():
                        print("Nazwisko musi zaczynać się z wielkiej litery.")
                        continue
                    break

                while True:
                    email = input("Proszę podać adres email: ")
                    if '@' not in email:
                        print("Email musi zawierać znak '@'.")
                        continue
                    break

                while True:
                    telefon = input("Proszę podać numer telefonu: ")
                    if not (telefon.isdigit() and len(telefon) == 9):
                        print("Numer telefonu musi składać się z 9 cyfr.")
                        continue
                    break

                haslo = input("Proszę podać hasło: ")

                # Dodanie użytkownika po pomyślnej walidacji wszystkich danych
                function.dodaj_uzytkownika(imie, nazwisko, email, telefon, haslo, connection)

            elif user_choice == 3:
                while True:
                    name = input("Podaj nazwę salonu : ")
                    address = input("Podaj lokalizację salonu : ")
                    service = input("Podaj nazwe uslugi : ")
                    if not name and not address and not service:
                        print("Musisz podac jeden z parametrow")
                        break
                    wyniki = function.wyszukaj_salony(connection, name, address,service)
                    displayed_salon_ids = []
                    if wyniki:
                        for salon in wyniki:
                            displayed_salon_ids.append(salon[0])
                            print(f"\nNazwa salonu: {salon[1]}")
                            print(f"Adres: {salon[2]}")
                            print(f"Właściciel: {salon[3]}")
                            print(f"Parking: {'Tak' if salon[4] == 1 else 'Nie'}")
                            print(f"Numer telefonu: {salon[5]}")
                            print(f"ID salonu: {salon[0]}")
                    else:
                        print("Nie znaleziono salonów spełniających podane kryteria")
                    break

            elif user_choice == 4:
                end_program = True


except Error as e:
    print("Błąd podczas połączenia z MySQL", e)