import mysql.connector
from mysql.connector import Error
from datetime import datetime


def connect():
    """
    Nawiązanie połączenia z bazą danych
    :return: connection
    """
    connection = mysql.connector.connect(host='127.0.0.1',
                                         database='Fryzjerzy',
                                         user='root',
                                         password='DUPA123')
    return connection


# pobranie oraz wyswietlenie danych z tabelki
# przy tworzeniu tabelki dodajemy
# objekt connection- odpowiedzialny za połączenie z nasza baza danych,
# table- nazwe tabeli jaka chcemy pokazac,
# selecet dana kolumne tabeli jaka chcemy pokazac (jesli nie wskazemy zadnej wyswietlią nasm sie wszytskie kolumny)
def show_data(connection, table, select="*"):
    # Tworzenie obiektu cursor
    cursor = connection.cursor()

    # Wykonywanie zapytania SQL
    cursor.execute(f"SELECT {select} FROM {table}")

    # Pobieranie wyników
    records = cursor.fetchall()

    # Wyświetlenie wyników
    for row in records:
        print(row)


def check_email_password(user_email, user_password, connection):
    """
    Funkcja sprawdzjąca czy istnieje adres email a takze czy pasuje do niego podane hasło
    :param user_email:
    :param user_password:
    :param connection:
    :return:
    """
    try:
        cursor = connection.cursor()
        query = "SELECT EXISTS(SELECT 1 FROM Users WHERE Email_address = %s)"  # sprawdzanie czy wystepuje podany email
        cursor.execute(query, (user_email,))
        outcome = cursor.fetchall()[0][0]

        if outcome == 1:
            query = "SELECT Password FROM Users WHERE Email_address = %s"  # jesli wystepuje sprawdzamy czy jest mu
            # przypisane podane hasło

            cursor.execute(query, (user_email,))

            password_in_db = cursor.fetchone()[0].strip()
            print("\n")
            if user_password == password_in_db:
                print("Udało Ci się pomyślnie zalogować.\n")
                return True
            else:
                print("Niepoprawne dane logowania. Spróbuj ponownie.\n")
                return False
        else:
            print("Niepoprawne dane logowania. Spróbuj ponownie.\n")


    except Error as e:
        print("Błąd podczas sprawdzania hasła!", e)
        return False
    finally:
        if cursor:
            cursor.close()


# funkcja pobiera dane user znając jedynie email uzytkownika
def fetch_user_data(user_email, connection):
    """
    Funkcja pobierająca dane o użytkowniku na podstawie jego adresu e-mail
    :param user_email:
    :param connection:
    :return:
    """
    try:
        cursor = connection.cursor()
        query = "SELECT User_ID, Name, Surname, Email_Address, Phone_Number, Password, Moderator, Administrator FROM Users WHERE Email_address = %s"
        cursor.execute(query, (user_email,))
        user_data = cursor.fetchone()
        return user_data


    except Error as e:
        print("Błąd podczas sprawdzania hasła.", e)
        return False

    finally:
        if cursor:
            cursor.close()


def user_action(user, connection):
    """
    Funkcja pozwalająca zwykłemu yżytkownikowi wybrać co chce zrobić
    :param user:
    :param connection:
    :return:
    """
    while True:
        print("1. Dodaj raport")
        print("2. Wyszukaj salon")
        print("3. Dodaj opinię")
        print("4. Wyswietl polubione salony")
        print("5. Wylogowanie się")
        print("6. Wyjście z programu")

        user_action = int(input("Wybierz jedną z dostępnych akcji: "))

        if user_action == 1:
            add_report(user, connection)
        elif user_action == 2:
            name = input("Podaj nazwę salonu: ")
            address = input("Podaj lokalizację salonu: ")
            service = input("Podaj usługę: ")
            if not name and not address and not service:
                print("Musisz podać jeden z parametrów")
                continue
            wyniki = wyszukaj_salony(connection, name, address, service)
            displayed_salon_ids = []
            if wyniki:
                for salon in wyniki:
                    displayed_salon_ids.append(salon[0])
                    print(f"\nNazwa salonu: {salon[1]}")
                    print(f"Adres: {salon[2]}")
                    print(f"Właściciel: {salon[3]}")
                    print(f"Parking: {'Tak' if salon[4] == 1 else 'Nie'}")
                    print(f"Numer telefonu: {salon[5]}")
                    print(f"Numer salonu: {salon[0]}")
            else:
                print("Nie znaleziono salonów spełniających podane kryteria")
                continue
            try:
                while True:
                    wybor_salonu = input(
                        "Podaj ID salonu, którego szczegółowe informacje chcesz zobaczyć (jeśli chcesz wyjść, wpisz 'n'): ")
                    if wybor_salonu.lower() == 'n':
                        break
                    wybor_salonu = int(wybor_salonu)
                    if wybor_salonu in displayed_salon_ids:
                        cursor = connection.cursor()

                        # Wyświetlanie opinii
                        cursor.execute("SELECT Stars_1_2_3_4_5, Description FROM Opinions WHERE Salon_ID = %s",
                                       (wybor_salonu,))
                        opinie = cursor.fetchall()
                        print("\nOpinie:")
                        for opinia in opinie:
                            print(f"Ocena: {opinia[0]}, Opis: {opinia[1]}")

                        # Wyświetlanie pracowników
                        print("\nPracownicy:")
                        user.show_workers(connection, wybor_salonu)  # Załóżmy, że show_workers to niezależna funkcja

                        # Wyświetlanie godzin otwarcia
                        print("\nGodziny otwarcia:")
                        user.show_opening_hour(connection,
                                               wybor_salonu)  # Załóżmy, że show_opening_hour to niezależna funkcja
                        print("\nUslugi w salonie:")
                        wyswietl_ceny_uslug_user(connection, wybor_salonu)
                        cursor.close()
                        break
                    else:
                        print("Możesz wyświetlić szczegółowe informacje tylko dla wyświetlonych salonów.")
            except ValueError:
                print("Nieprawidłowy wybór, to nie jest liczba.")
            displayed_salon_ids = []
            if wyniki:
                for salon in wyniki:
                    displayed_salon_ids.append(salon[0])
                    print(f"\nNazwa salonu: {salon[1]}")
                    print(f"Adres: {salon[2]}")
                    print(f"Właściciel: {salon[3]}")
                    print(f"Parking: {'Tak' if salon[4] == 1 else 'Nie'}")
                    print(f"Numer telefonu: {salon[5]}")
                    print(f"Numer salonu (ID): {salon[0]}")  # Wyświetlenie ID salonu
            else:
                print("Nie znaleziono salonów spełniających podane kryteria")
                continue

            while True:
                wybor_salonu = input(
                    "Czy chcesz dodać któryś z salonów do ulubionych? Wpisz ID salonu lub 'n', aby zrezygnować: ")
                if wybor_salonu.isdigit() and int(wybor_salonu) in displayed_salon_ids:
                    dodaj_do_ulubionych(connection, user.User_ID, int(wybor_salonu))
                    break
                elif wybor_salonu == "n":
                    break
                else:
                    print("Możesz dodać salon do ulubionych tylko dla wyświetlonych salonów.")

        elif user_action == 3:
            name = input("Podaj nazwę salonu: ")
            address = input("Podaj lokalizację salonu: ")
            service = input("Podaj usługę: ")
            if not name and not address and not service:
                print("Musisz podać jeden z parametrów")
                continue
            wyniki = wyszukaj_salony(connection, name, address, service)
            displayed_salon_ids = []
            if wyniki:
                for salon in wyniki:
                    displayed_salon_ids.append(salon[0])
                    print(f"\nNazwa salonu: {salon[1]}")
                    print(f"Adres: {salon[2]}")
                    print(f"Właściciel: {salon[3]}")
                    print(f"Parking: {'Tak' if salon[4] == 1 else 'Nie'}")
                    print(f"Numer telefonu: {salon[5]}")
                    print(f"Numer salonu: {salon[0]}")
            else:
                print("Nie znaleziono salonów spełniających podane kryteria")
                continue
            add_opinion(user, connection)

        elif user_action == 5:
            return 'logout'

        elif user_action == 6:
            connection.close()
            exit()

        elif user_action == 4:
            pokaz_ulubione_salony(user, connection)

        else:
            print("Nieprawidłowy wybór. Wybierz ponownie.")


def ustaw_cene_uslugi(connection, user, service_id, cena):
    if user.Moderator:
        try:
            cursor = connection.cursor()

            # Sprawdzenie, czy taka kombinacja Service_ID i Salon_ID już istnieje
            cursor.execute("SELECT Price_ID FROM Prices WHERE Service_ID = %s AND Salon_ID = %s", (service_id, user.Moderator))
            istnieje = cursor.fetchone()

            if istnieje:
                # Aktualizacja ceny, jeśli kombinacja już istnieje
                query = "UPDATE Prices SET Price = %s WHERE Service_ID = %s AND Salon_ID = %s"
                cursor.execute(query, (cena, service_id, user.Moderator))
            else:
                # Dodanie nowego wpisu, jeśli kombinacja nie istnieje
                query = "INSERT INTO Prices (Service_ID, Salon_ID, Price) VALUES (%s, %s, %s)"
                cursor.execute(query, (service_id, user.Moderator, cena))

            connection.commit()
            print("Cena usługi została zaktualizowana.")

        except Exception as e:
            print(f"Błąd podczas aktualizowania ceny usługi: {e}")
        finally:
            if cursor:
                cursor.close()
    else:
        print("Nie masz uprawnień do zmiany cen usług w tym salonie.")


def pokaz_ulubione_salony(self, connection):
    cursor = connection.cursor()

    # Zakładam, że istnieje tabela 'UlubioneSalony' z kolumną 'User_ID' i 'Salon_ID'
    try:
        cursor.execute("SELECT Salon_ID FROM Liked_Salons WHERE User_ID = %s", (self.User_ID,))
        ulubione_salony = cursor.fetchall()

        if ulubione_salony:
            print("Twoje ulubione salony:")
            for salon in ulubione_salony:
                # Pobieranie informacji o każdym salonie
                cursor.execute("SELECT * FROM Hair_Salon WHERE Salon_ID = %s", (salon[0],))
                informacje_o_salonie = cursor.fetchone()
                print(
                    f"Salon ID: {informacje_o_salonie[0]}, Nazwa: {informacje_o_salonie[1]}, Adres: {informacje_o_salonie[2]}")
        else:
            print("Nie masz jeszcze ulubionych salonów.")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

    finally:
        if cursor:
            cursor.close()


def add_report(user, connection):
    cursor = connection.cursor()

    # Pobranie najwyższego Report_ID i inkrementacja
    try:
        cursor.execute("SELECT MAX(Report_ID) FROM Reports")
        max_id_result = cursor.fetchone()
        next_report_id = (max_id_result[0] or 0) + 1
        user_id = user._get_user_id()
    except Error as e:
        print("Wystąpił błąd przy odczytywaniu maksymalnego Report_ID:", e)
        return

    # Prośba o pozostałe dane od użytkownika
    # user_id = input("Podaj User_ID: ")
    report_description = input("\nPodaj opis raportu: ")

    # Uzyskanie aktualnej daty i czasu
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Tworzenie i wykonanie zapytania SQL
    add_report_query = """
    INSERT INTO Reports (Report_ID, User_ID, Report_Date, Report_Description)
    VALUES (%s, %s, %s, %s)
    """
    data = (next_report_id, user_id, current_time, report_description)

    try:
        cursor.execute(add_report_query, data)
        connection.commit()  # Zatwierdzenie transakcji
        print("Raport został dodany z Report_ID:", next_report_id)
        print("\n")
    except Error as e:
        print("Wystąpił błąd przy dodawaniu raportu:", e)

    cursor.close()


def dodaj_do_ulubionych(connection, user_id, salon_id):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO Liked_Salons (User_ID, Salon_ID) VALUES (%s, %s)"
        cursor.execute(query, (user_id, salon_id))
        connection.commit()
        print("Salon został dodany do ulubionych.")
    except Error as e:
        print("Błąd podczas dodawania salonu do ulubionych:", e)
    finally:
        if cursor:
            cursor.close()


def dodaj_uzytkownika(name, surname, email_address, phone_number, password, connection):
    try:
        cursor = connection.cursor()
        query = ("INSERT INTO Users (Name, Surname, Email_Address, Phone_Number, Password, Moderator, Administrator) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        values = (name, surname, email_address, phone_number, password, 0, 0)
        cursor.execute(query, values)
        connection.commit()
        print("Użytkownik został dodany pomyślnie.")
    except Error as e:
        print("Błąd podczas dodawania użytkownika do bazy danych:", e)
    finally:
        if cursor:
            cursor.close()


def dodaj_salon(connection):
    cursor = connection.cursor()
    # Pobranie najwyższego ID salonu i inkrementacja
    cursor.execute("SELECT MAX(Salon_ID) FROM Hair_Salon")
    max_id_result = cursor.fetchone()
    next_salon_id = (max_id_result[0] or 0) + 1
    salon_id = next_salon_id

    name = input("Podaj nazwę salonu: ")
    address = input("Podaj adres salonu: ")
    owner = input("Podaj właściciela salonu: ")
    parking_lot = input("Czy jest parking (1/0): ")
    phone_no = input("Podaj numer telefonu salonu: ")
    salon_data = (salon_id, name, address, owner, parking_lot, phone_no)

    try:
        cursor = connection.cursor()
        query = "INSERT INTO Hair_Salon (Salon_ID, Name, Address, Owner, Has_Parking, Phone_Number) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, salon_data)
        connection.commit()
        print("Salon został pomyślnie dodany z ID:", next_salon_id)
    except Error as e:
        print("Błąd podczas dodawania salonu:", e)


def aktualizuj_salon(connection, user):
    if user.Moderator:
        salon_id = user.Moderator  # user.moderator przechowuje ID salonu
        print("\nJesteś moderatorem salonu nr: ", salon_id)
        print("Zaktualizuj dane salonu\n")

        # Przykład danych, które moderator może chcieć zaktualizować
        new_name = input("Podaj nową nazwę salonu (lub zostaw puste): ")
        new_address = input("Podaj nowy adres (lub zostaw puste): ")
        new_owner = input("Podaj nowego wlasciciela (lub zostaw puste): ")
        new_has_parking = input("Podaj nowa wartosc parkingu 0/1 (lub zostaw puste): ")
        new_phone = input("Podaj nowy numer telefonu (lub zostaw puste): ")
        # Dodaj więcej pól według potrzeb

        updated_data = {}
        if new_name:
            updated_data["Name"] = new_name
        if new_address:
            updated_data["Address"] = new_address
        if new_owner:
            updated_data["Owner"] = new_owner
        if new_has_parking:
            updated_data["Has_Parking"] = new_has_parking
        if new_phone:
            updated_data["Phone_Number"] = new_phone
            # Dodaj więcej pól do słownika updated_data, jeśli są

        if updated_data:
            try:
                cursor = connection.cursor()
                # Przygotowanie zapytania SQL
                updates = ", ".join([f"{key} = %s" for key in updated_data])
                values = list(updated_data.values())
                values.append(salon_id)

                query = f"UPDATE Hair_Salon SET {updates} WHERE Salon_ID = %s"
                cursor.execute(query, values)
                connection.commit()
                print("Dane salonu zostały zaktualizowane.")
            except Error as e:
                print("Błąd podczas aktualizacji danych salonu:", e)
            finally:
                if cursor:
                    cursor.close()
        else:
            print("Brak danych do aktualizacji")
    else:
        print("Nie masz uprawnien do edycji danych tego salonu")


def wyszukaj_salony(connection, name=None, address=None, service_name=None):
    try:
        cursor = connection.cursor()
        query = "SELECT DISTINCT Hair_Salon.* FROM Hair_Salon"
        query_conditions = []
        values = []

        # Dodanie warunku związanego z nazwą salonu
        if name:
            query_conditions.append(" Hair_Salon.Name LIKE %s")
            values.append(f"%{name}%")

        # Dodanie warunku związanego z adresem salonu
        if address:
            query_conditions.append(" Hair_Salon.Address LIKE %s")
            values.append(f"%{address}%")

        # Dodanie warunku związanego z nazwą usługi
        if service_name:
            query += " JOIN Salon_Services ON Hair_Salon.Salon_ID = Salon_Services.Salon_ID"
            query += " JOIN Services ON Salon_Services.Service_ID = Services.Service_ID"
            query_conditions.append(" Services.Name LIKE %s")
            values.append(f"%{service_name}%")

        # Dodanie warunków do zapytania, jeśli istnieją
        if query_conditions:
            query += " WHERE " + ' AND '.join(query_conditions)

        cursor.execute(query, tuple(values))

        results = cursor.fetchall()
        if results:
            return results
        else:
            print("Nie znaleziono salonów spełniających podane kryteria.")
            return []

    except Error as e:
        print("Błąd podczas wyszukiwania salonów:", e)
        return []
    finally:
        if cursor:
            cursor.close()


def zarzadzaj_uslugami(connection, user):
    if user.Administrator:
        while True:
            print("\nZarządzanie usługami:")
            print("1: Wyświetl dostępne usługi")
            print("2: Dodaj nową usługę")
            print("3: Usuń istniejącą usługę")
            print("4: Wróć do poprzedniego menu")

            wybor = input("Wybierz opcję: ")

            if wybor == "1":
                wyswietl_uslugi(connection)
            elif wybor == "2":
                dodaj_usluge(connection)
            elif wybor == "3":
                usun_usluge(connection)
            elif wybor == "4":
                break
            else:
                print("Nieprawidłowy wybór. Spróbuj ponownie.")
    else:
        print("Nie masz uprawnień do zarządzania usługami.")


def wyswietl_uslugi(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM Services"
        cursor.execute(query)
        services = cursor.fetchall()
        if services:
            print("Lista dostępnych usług:")
            for service in services:
                print(f"ID: {service[0]}, Nazwa: {service[1]}, Opis: {service[2]}")
        else:
            print("Brak dostępnych usług.")
    except Error as e:
        print("Błąd podczas wyświetlania usług:", e)
    finally:
        if cursor:
            cursor.close()


def dodaj_usluge(connection):
    nazwa_uslugi = input("Podaj nazwę usługi: ")
    opis_uslugi = input("Podaj opis usługi: ")

    try:
        cursor = connection.cursor()
        query = "INSERT INTO Services (Name, Description) VALUES (%s, %s)"
        cursor.execute(query, (nazwa_uslugi, opis_uslugi))
        connection.commit()
        print("Usługa została dodana pomyślnie.")
    except Error as e:
        print("Błąd podczas dodawania usługi:", e)
    finally:
        if cursor:
            cursor.close()


def usun_usluge(connection):
    nazwa_uslugi = input("Podaj nazwę usługi do usunięcia: ")

    try:
        cursor = connection.cursor()
        query = "DELETE FROM Services WHERE Name = %s"
        cursor.execute(query, (nazwa_uslugi,))
        connection.commit()

        if cursor.rowcount:
            print("Usługa została usunięta pomyślnie.")
        else:
            print("Nie znaleziono usługi o tej nazwie.")
    except Error as e:
        print("Błąd podczas usuwania usługi:", e)
    finally:
        if cursor:
            cursor.close()


def zarzadzaj_uslugami_salonu(connection, user):
    if user.Moderator:
        while True:
            print("\nZarządzanie usługami:")
            print("1: Wyświetl usugi dostepne w twoim salonie")
            print("2: Dodaj nową usługę do salonu")
            print("3: Usuń istniejącą usługę")
            print("4: Wróć do poprzedniego menu")

            wybor = input("Wybierz opcję: ")

            if wybor == "1":
                wyswietl_uslugi_salonu(connection, user)
            elif wybor == "2":
                dodaj_usluge_do_salonu(connection, user)
            elif wybor == "3":
                usun_usluge_z_salonu(connection, user)
            elif wybor == "4":
                break
            else:
                print("Nieprawidłowy wybór. Spróbuj ponownie.")
    else:
        print("Nie masz uprawnień do zarządzania usługami salonu.")


def wyswietl_uslugi_salonu(connection, user, salon_id=None):
    selected_salon_id = salon_id if salon_id is not None else user.Moderator

    try:
        cursor = connection.cursor()

        query = """
        SELECT Services.Service_ID, Services.Name 
        FROM Services
        JOIN Salon_Services ON Services.Service_ID = Salon_Services.Service_ID
        WHERE Salon_Services.Salon_ID = %s
        """
        cursor.execute(query, (selected_salon_id,))
        uslugi = cursor.fetchall()

        if not uslugi:
            print(f"W salonie o ID {selected_salon_id} nie ma jeszcze usług.")
            return

        print(f"Usługi w salonie o ID {selected_salon_id}:")
        for usluga in uslugi:
            # Sprawdzenie, czy krotka ma przynajmniej dwa elementy
            if len(usluga) >= 2:
                print(f"ID usługi: {usluga[0]}, Nazwa usługi: {usluga[1]}")
            else:
                print("Błąd danych usługi.")

    except Exception as e:
        print(f"Błąd podczas wyświetlania usług salonu: {e}")

    finally:
        if cursor:
            cursor.close()


def wyswietl_ceny_uslug(connection, salon_id):
    try:
        cursor = connection.cursor()

        # Wyświetlenie cen usług dla danego salonu
        query = """
        SELECT Services.Service_ID, Services.Name, Prices.Price
        FROM Services
        JOIN Prices ON Services.Service_ID = Prices.Service_ID
        WHERE Prices.Salon_ID = %s
        """
        cursor.execute(query, (salon_id,))
        ceny_uslug = cursor.fetchall()

        if not ceny_uslug:
            print(f"W salonie o ID {salon_id} nie ma jeszcze ustalonych cen usług.")
            return

        print(f"Ceny usług w salonie o ID {salon_id}:")
        for cena_uslugi in ceny_uslug:
            print(f"ID usługi: {cena_uslugi[0]}, Nazwa usługi: {cena_uslugi[1]}, Cena: {cena_uslugi[2]}")

    except Exception as e:
        print(f"Błąd podczas wyświetlania cen usług: {e}")

    finally:
        if cursor:
            cursor.close()


def wyswietl_ceny_uslug_user(connection, salon_id):
    try:
        cursor = connection.cursor()

        # Wyświetlenie cen usług dla danego salonu
        query = """
        SELECT Services.Service_ID, Services.Name, Prices.Price
        FROM Services
        JOIN Prices ON Services.Service_ID = Prices.Service_ID
        WHERE Prices.Salon_ID = %s
        """
        cursor.execute(query, (salon_id,))
        ceny_uslug = cursor.fetchall()

        if not ceny_uslug:
            print(f"W salonie o ID {salon_id} nie ma jeszcze ustalonych cen usług.")
            return

        for cena_uslugi in ceny_uslug:
            print(f"Nazwa usługi: {cena_uslugi[1]}, Cena: {cena_uslugi[2]}")

    except Exception as e:
        print(f"Błąd podczas wyświetlania cen usług: {e}")

    finally:
        if cursor:
            cursor.close()


def aktualizuj_ceny_uslug(connection, user):
    if not user.Moderator:
        print("Nie masz uprawnień do aktualizacji cen usług.")
        return

    try:
        cursor = connection.cursor()

        # Pobranie listy usług dla salonu
        query = """
        SELECT Services.Service_ID, Services.Name 
        FROM Services
        JOIN Salon_Services ON Services.Service_ID = Salon_Services.Service_ID
        WHERE Salon_Services.Salon_ID = %s
        """
        cursor.execute(query, (user.Moderator,))
        uslugi = cursor.fetchall()

        if not uslugi:
            print(f"W salonie o ID {user.Moderator} nie ma jeszcze usług.")
            return

        print(f"Aktualizacja cen usług w salonie o ID {user.Moderator}:")
        for usluga in uslugi:
            print(f"Usługa: {usluga[1]} (ID: {usluga[0]})")
            nowa_cena = float(input("Podaj nową cenę dla tej usługi: "))

            # Aktualizacja ceny usługi
            update_query = "UPDATE Prices SET Price = %s WHERE Service_ID = %s AND Salon_ID = %s"
            cursor.execute(update_query, (nowa_cena, usluga[0], user.Moderator))

        connection.commit()
        print("Ceny usług zostały zaktualizowane.")

    except Exception as e:
        print(f"Błąd podczas aktualizacji cen usług: {e}")
        connection.rollback()

    finally:
        if cursor:
            cursor.close()


def dodaj_usluge_do_salonu(connection, user):
    if user.Moderator:
        try:
            cursor = connection.cursor()

            # Wyświetlenie dostępnych usług
            cursor.execute("SELECT * FROM Services")
            uslugi = cursor.fetchall()
            print("Dostępne usługi:")
            for usluga in uslugi:
                print(f"ID: {usluga[0]}, Nazwa: {usluga[1]}")

            # Wybór usługi do dodania
            usluga_id = input("Podaj ID usługi do dodania do Twojego salonu: ")

            # Dodanie usługi do salonu
            query = "INSERT INTO Salon_Services (Salon_ID, Service_ID) VALUES (%s,%s)"
            cursor.execute(query, (user.Moderator, usluga_id))
            connection.commit()
            print("Usługa została dodana do Twojego salonu.")
        except Error as e:
            print("Błąd podczas dodawania usługi do salonu:", e)
        finally:
            if cursor:
                cursor.close()
    else:
        print("Nie masz uprawnień do dodawania usługi do salonu.")


def usun_usluge_z_salonu(connection, user):
    if user.Moderator:
        try:
            cursor = connection.cursor()

            # Wyświetlenie usług przypisanych do salonu
            query = """
            SELECT Services.Service_ID, Services.Name
            FROM Services
            JOIN Salon_Services ON Services.Service_ID = Salon_Services.Service_ID
            WHERE Salon_Services.Salon_ID = %s
            """
            cursor.execute(query, (user.Moderator,))
            uslugi = cursor.fetchall()
            print("Usługi w Twoim salonie:")
            for usluga in uslugi:
                print(f"ID usługi: {usluga[0]}, Nazwa usługi: {usluga[1]}")

            # Wybór usługi do usunięcia
            usluga_id = input("Podaj ID usługi do usunięcia z Twojego salonu: ")

            # Usunięcie usługi z salonu
            query = "DELETE FROM Salon_Services WHERE Salon_ID = %s AND Service_ID = %s"
            cursor.execute(query, (user.Moderator, usluga_id))
            connection.commit()
            print("Usługa została usunięta z Twojego salonu.")

        except Error as e:
            print("Błąd podczas usuwania usługi z salonu:", e)
        finally:
            if cursor:
                cursor.close()
    else:
        print("Nie masz uprawnień do usuwania usługi z salonu.")


def add_opinion(user, connection):
    cursor = connection.cursor()

    # Pobranie najwyższego Opinion_ID i inkrementacja
    try:
        cursor.execute("SELECT MAX(Opinion_ID) FROM Opinions")
        max_id_result = cursor.fetchone()
        next_opinion_id = (max_id_result[0] or 0) + 1
        user_id = user._get_user_id()
    except Error as e:
        print("Wystąpił błąd przy odczytywaniu maksymalnego Opinion_ID:", e)
        return

    salon_id = int(input("Podaj ID salonu do ktorego chcesz dodac opinie: "))

    cursor.execute("SELECT 1 FROM Hair_Salon WHERE Salon_ID = %s", (salon_id,))
    if not cursor.fetchone():
        print("Salon o podanym ID nie istnieje.")
        return

    opinion_description = input("Podaj opis opinii: ")
    stars = int(input("Wybierz ilosc gwiazdek dla salonu (1-5): "))

    # Tworzenie i wykonanie zapytania SQL
    add_report_query = """
    INSERT INTO Opinions (Opinion_ID, User_ID, Salon_ID, Stars_1_2_3_4_5, Description)
    VALUES (%s, %s, %s, %s, %s)
    """
    data = (next_opinion_id, user_id, salon_id, stars, opinion_description)

    try:
        cursor.execute(add_report_query, data)
        connection.commit()  # Zatwierdzenie transakcji
        print("Opinia została dodana z Opinion_ID:", next_opinion_id)
    except Error as e:
        print("Wystąpił błąd przy dodawaniu opinii:", e)

    cursor.close()


def przeglądaj_opinie(connection):
    try:
        salon_id = int(input("Podaj Salon_ID, którego opinie chcesz przeglądać: "))
    except ValueError:
        print("Podano nieprawidłowy Salon_ID. Proszę podać liczbę całkowitą.")
        return

    cursor = connection.cursor()
    query = "SELECT Opinion_ID, User_ID, Salon_ID, Stars_1_2_3_4_5, Description FROM Opinions WHERE Salon_ID = %s"

    try:
        cursor.execute(query, (salon_id,))
        opinie = cursor.fetchall()

        if opinie:
            for opinia in opinie:
                print("Opinion ID:", opinia[0], "User ID:", opinia[1], "Salon ID:", opinia[2], "Stars:", opinia[3],
                      "Description:", opinia[4])
        else:
            print("Nie ma opinii dla salonu o ID:", salon_id)
    except Exception as e:
        print("Wystąpił błąd podczas dostępu do bazy danych:", e)


def przeglądaj_raporty(connection):
    cursor = connection.cursor()
    query = "SELECT Report_ID, User_ID, Report_Date, Report_Description FROM Reports ORDER BY Report_Date DESC"

    try:
        cursor.execute(query)
        raporty = cursor.fetchall()

        if raporty:
            for raport in raporty:
                print("Report ID:", raport[0], "User ID:", raport[1], "Report Date:", raport[2], "Description:",
                      raport[3])
        else:
            print("Nie ma żadnych raportów.")
    except Exception as e:
        print("Wystąpił błąd podczas dostępu do bazy danych:", e)
    finally:
        cursor.close()


def wyswietl_ceny_uslug_user(connection, salon_id):
    try:
        cursor = connection.cursor()

        # Wyświetlenie cen usług dla danego salonu
        query = """
        SELECT Services.Service_ID, Services.Name, Prices.Price
        FROM Services
        JOIN Prices ON Services.Service_ID = Prices.Service_ID
        WHERE Prices.Salon_ID = %s
        """
        cursor.execute(query, (salon_id,))
        ceny_uslug = cursor.fetchall()

        if not ceny_uslug:
            print(f"W salonie o ID {salon_id} nie ma jeszcze ustalonych cen usług.")
            return

        for cena_uslugi in ceny_uslug:
            print(f"Nazwa usługi: {cena_uslugi[1]}, Cena: {cena_uslugi[2]}")

    except Exception as e:
        print(f"Błąd podczas wyświetlania cen usług: {e}")

    finally:
        if cursor:
            cursor.close()


def wyswietl_czasy_uslug(connection, salon_id):
    try:
        cursor = connection.cursor()

        # Wyświetlenie przybliżonego czasu trwania usług dla danego salonu
        query = """
        SELECT Services.Service_ID, Services.Name, Approx_Time.Time
        FROM Services
        JOIN Approx_Time ON Services.Service_ID = Approx_Time.Service_ID
        WHERE Approx_Time.Salon_ID = %s
        """
        cursor.execute(query, (salon_id,))
        czasy_uslug = cursor.fetchall()

        if not czasy_uslug:
            print(f"W salonie o ID {salon_id} nie ma jeszcze ustalonych przybliżonych czasów usług.")
            # return

        print(f"\nPrzybliżone czasy usług w salonie o ID {salon_id}:")

        for czas_uslugi in czasy_uslug:
            print(f"ID usługi: {czas_uslugi[0]}, Nazwa usługi: {czas_uslugi[1]}, Przybliżony czas: {czas_uslugi[2]}\n")

    except Exception as e:
        print(f"Błąd podczas wyświetlania przybliżonych czasów usług: {e}")

    finally:
        if cursor:
            cursor.close()


def ustaw_czas_uslugi(connection, user, service_id, czas):
    if user.Moderator:
        try:
            cursor = connection.cursor()

            # Sprawdzenie, czy taka kombinacja Service_ID i Salon_ID już istnieje
            cursor.execute("SELECT * FROM Approx_Time WHERE Service_ID = %s AND Salon_ID = %s",
                           (service_id, user.Moderator))
            istnieje = cursor.fetchone()

            if istnieje:
                # Aktualizacja czasu, jeśli kombinacja już istnieje
                query = "UPDATE Approx_Time SET Time = %s WHERE Service_ID = %s AND Salon_ID = %s"
                cursor.execute(query, (czas, service_id, user.Moderator))
            else:
                # Dodanie nowego wpisu, jeśli kombinacja nie istnieje
                query = "INSERT INTO Approx_Time (Service_ID, Salon_ID, Time) VALUES (%s, %s, %s)"
                cursor.execute(query, (service_id, user.Moderator, czas))

            connection.commit()
            print("Czas usługi został zaktualizowany.")

        except Exception as e:
            print(f"Błąd podczas aktualizowania czasu usługi: {e}")
        finally:
            if cursor:
                cursor.close()
    else:
        print("Nie masz uprawnień do zmiany czasu usług w tym salonie.")


def show_workers(connection, nazwa_salonu):
    cursor = connection.cursor()
    values = []
    values.append(nazwa_salonu)
    # Wykonywanie zapytania SQL
    query = f"SELECT Workers.Name, Workers.Surname, Workers.Description, Hair_Salon.Name," \
            f" Hair_Salon.Address, Hair_Salon.Owner FROM Workers join Hair_Salon on " \
            f"(Hair_Salon.Salon_ID=Workers.Salon_ID) WHERE Hair_Salon.Name = %s"

    cursor.execute(query, values)

    # Pobieranie wyników
    records = cursor.fetchall()

    # Wyświetlenie wyników
    for row in records:
        print(f"{row[0]} {row[1]} \nOpis: {row[2]} \nSalon: {row[3]}\n")


def show_opening_hour(connection, nazwa_salonu):
    cursor = connection.cursor()

    values = []
    values.append(nazwa_salonu)
    # Wykonywanie zapytania SQL
    query = f"SELECT Opening_Hours.ID, Opening_Hours.Salon_ID, Opening_Hours.Week_Day, " \
            f"Opening_Hours.Opening_Hour, Opening_Hours.Closing_Hour FROM Opening_Hours join Hair_Salon" \
            f" on (Hair_Salon.Salon_ID=Opening_Hours.Salon_ID) WHERE Hair_Salon.Name = %s"

    cursor.execute(query, values)

    # Pobieranie wyników
    records = cursor.fetchall()

    # Wyświetlenie wyników
    for row in records:
        id, salon_id, week_day, open, close = row[0], row[1], row[2], row[3], row[4]
        total_seconds = int(open.total_seconds())

        # Obliczanie godzin i minut
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        # Formatowanie i wyświetlanie wyniku
        formatted_time1 = f"{hours}:{minutes:02d}"

        total_seconds = int(close.total_seconds())
        # Obliczanie godzin i minut
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        # Formatowanie i wyświetlanie wyniku
        formatted_time2 = f"{hours}:{minutes:02d}"

        print(f"{week_day}: {formatted_time1}-{formatted_time2}")


def show_exceptions(connection, nazwa_salonu):
    cursor = connection.cursor()
    values = []
    values.append(nazwa_salonu)
    # Wykonywanie zapytania SQL
    query = f"SELECT Exceptions.Opening_Hour, Exceptions.Closing_Hour, Exceptions.Starting_Date," \
            f" Exceptions.Ending_Date FROM Exceptions join Hair_Salon on (Hair_Salon.Salon_ID=Exceptions.Salon_ID)" \
            f" WHERE Hair_Salon.Name = %s"

    cursor.execute(query, values)

    # Pobieranie wyników
    records = cursor.fetchall()


    # Wyświetlenie wyników
    for row in records:
        total_seconds = int(row[0].total_seconds())

        # Obliczanie godzin i minut
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        # Formatowanie i wyświetlanie wyniku
        formatted_time1 = f"{hours}:{minutes:02d}"

        total_seconds = int(row[1].total_seconds())
        # Obliczanie godzin i minut
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        # Formatowanie i wyświetlanie wyniku
        formatted_time2 = f"{hours}:{minutes:02d}"
        print(f"{row[2]} - {row[3]} \n{formatted_time1}-{formatted_time2}\n")
