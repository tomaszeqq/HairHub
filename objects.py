from mysql.connector import Error

class User:
    def __init__(self, User_ID, Name, Surname, Email_Address, Phone_Number, Password, Moderator, Administrator):
        self.User_ID = User_ID
        self.Name = Name
        self.Surname = Surname
        self.Email_Address = Email_Address
        self.Phone_Number = Phone_Number
        self.Password = Password
        self.Moderator = Moderator
        self.Administrator = Administrator

    def _get_user_id(self):
        return self.User_ID

    def __str__(self):
        return (f"User ID: {self.User_ID}\n"
                f"Name: {self.Name}\n"
                f"Surname: {self.Surname}\n"
                f"Email Address: {self.Email_Address}\n"
                f"Phone Number: {self.Phone_Number}\n"
                f"Password: {self.Password}\n"
                f"Moderator: {self.Moderator}\n"
                f"Administrator: {self.Administrator}\n")

    def show_workers(self, connection, salon_id=None):
        cursor = connection.cursor()

        # Ustalanie ID salonu
        selected_salon_id = salon_id if salon_id is not None else self.Moderator

        # Wykonywanie zapytania SQL
        cursor.execute(f"SELECT * FROM Workers WHERE Salon_ID = {selected_salon_id}")

        # Pobieranie wyników
        records = cursor.fetchall()

        # Wyświetlenie wyników, pomijając dwa pierwsze pola
        for row in records:
            # Tworzenie formatowanego stringa z danych pracownika, pomijając pierwsze dwa pola
            formatted_row = ', '.join(map(str, row[2:]))
            print(formatted_row)

    def zarzadzaj_pracownikami(self,connection):
        a=True
        while a:
            print("\nCo chcesz uczynić:\n"
                  "1: dodaj pracownika\n"
                  "2: usun pracownika\n"
                  "3: edytuj dane pracownika\n"
                  "4: pokaż liste pracowników\n"
                  "5: powróć do poprzedniego menu:\n"
                )
            choice=input()
            if choice=="4":
                self.show_workers(connection)
            elif choice=="1":
                self.dodaj_pracownika(connection)
            elif choice=="3":
                self.edytuj_dane_pracownika(connection)
            elif choice=="2":
                self.usun_pracownika(connection)
            elif choice=="5":
                break

    def dodaj_pracownika(self, connection):
        if self.Moderator:
            try:
                cursor = connection.cursor()

                # # Wyświetlenie
                # self.show_workers(connection)


                # Dodanie pracownika
                while True:
                    imie = input("Proszę podać imię pracownika: ")
                    if imie.istitle():
                        break
                    else:
                        print("Imię musi zaczynać się z wielkiej litery.")

                    # Prośba o nazwisko z walidacją
                while True:
                    nazwisko = input("Proszę podać nazwisko pracownika: ")
                    if nazwisko.istitle():
                        break
                    else:
                        print("Nazwisko musi zaczynać się z wielkiej litery.")

                    # Prośba o opis
                opis = input("Proszę podać opis dla nowego pracownika: ")

                # Dodanie pracownika
                query = "INSERT INTO Workers (Salon_ID, Name, Surname, Description) VALUES (%s,%s,%s,%s)"
                cursor.execute(query, (self.Moderator, imie, nazwisko, opis))
                connection.commit()
                print("Nowy pracownik został dodany.")
            except Error as e:
                print("Błąd podczas dodawania nowego pracownika:", e)

            finally:
                if cursor:
                    cursor.close()

    def edytuj_dane_pracownika(self, connection):
            if self.Moderator:
                self.show_workers(connection)
                worker_id=int(input("Podaj ID pracownika którego dane chcesz edytować: "))

                # Przykład danych, które moderator może chcieć zaktualizować
                new_name = input("Podaj nowe imie pracownika (lub zostaw puste): ")
                new_surname = input("Podaj nowe nazwisko  (lub zostaw puste): ")
                new_description = input("Podaj nowey opisa pracownika (lub zostaw puste): ")

                # Dodaj więcej pól według potrzeb
                updated_data = {}
                if new_name:
                    updated_data["Name"] = new_name
                if new_surname:
                    updated_data["Surname"] = new_surname
                if new_description:
                    updated_data["Description"] = new_description

                if updated_data:
                    try:
                        cursor = connection.cursor()
                        # Przygotowanie zapytania SQL
                        updates = ", ".join([f"{key} = %s" for key in updated_data])
                        values = list(updated_data.values())
                        values.append(self.Moderator)
                        values.append(int(worker_id))

                        query = f"UPDATE Workers SET {updates} WHERE Salon_ID = %s AND Worker_ID = %s"
                        cursor.execute(query, values)
                        connection.commit()
                        print("Dane pracownika zostały zaktualizowane.")
                    except Error as e:
                        print("Błąd podczas aktualizacji danych pracownika:", e)
                    finally:
                        if cursor:
                            cursor.close()
                else:
                    print("Brak danych do aktualizacji")
            else:
                print("Nie masz uprawnien do edycji danych tego pracownika")

    def usun_pracownika(self, connection):
        if self.Moderator:
            self.show_workers(connection)
            worker_id=int(input("Podaj ID pracownika którego dane chcesz usunąć ze swojego salonu: "))
            try:
                cursor = connection.cursor()

                # Usunięcie pracownika
                query = "DELETE FROM Workers WHERE Salon_ID = %s AND Worker_ID = %s"
                cursor.execute(query, (int(self.Moderator), worker_id))
                connection.commit()
                print("Pracownik został usunięty.")
            except Error as e:
                print("Błąd podczas usuwania pracownika:", e)
            finally:
                if cursor:
                    cursor.close()
        else:
            print("Nie masz uprawnień do usuwania pracowników.")

    def show_opening_hour(self, connection, salon_id=None):
        cursor = connection.cursor()

        # Ustalanie ID salonu
        selected_salon_id = salon_id if salon_id is not None else self.Moderator

        # Wykonywanie zapytania SQL
        cursor.execute(f"SELECT * FROM Opening_Hours WHERE Salon_ID = {selected_salon_id}")

        # Pobieranie wyników
        records = cursor.fetchall()

        # Wyświetlenie wyników
        for row in records:
            id, salon_id, week_day, open, close = row[0], row[1], row[2], row[3], row[4]
            total_seconds = int(open.total_seconds())

            # Obliczanie godzin i minut
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            formatted_time_open = f"{hours}:{minutes:02d}"

            total_seconds = int(close.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            formatted_time_close = f"{hours}:{minutes:02d}"

            print(f"{week_day}: {formatted_time_open}-{formatted_time_close}")

    def zarzadzaj_wyjątkami(self, connection):
        a = True
        while a:
            print("\nCo chcesz uczynić:\n"
                  "1: Ustaw nowe wyjątek dla swojego salonu \n"
                  "2: Usuń istniejący wyjątek\n"
                  "3: Wyświetl istniejące wyjątki \n"
                  "4: powróć do poprzedniego menu: \n"
                  )
            choice = input()
            if choice == "1":
                self.dodaj_wyjątek(connection)
            elif choice == "2":
                self.usun_wyjątek(connection)
            elif choice == "3":
                self.show_exceptions(connection)
            elif choice == "4":
                break

    def zarzadzaj_godzinami_otwarcia(self, connection):
        a = True
        while a:
            print("\nCo chcesz uczynić:\n"
                  "1: Ustaw nowe Godziny otwarcia dla salonu \n"
                  "2: Mdyfikuj obecne godziny otwarcia \n"
                  "3: Wyświetl obecne godziny otwarcia \n"
                  "4: Zarządzaj wyjątkami \n"
                  "5: powróć do poprzedniego menu: \n"
                  )
            choice = input()
            if choice == "3":
                self.show_opening_hour(connection)
            elif choice == "1":
                self.ustaw_nowe_godziny_otwarcia(connection)
            elif choice == "2":
                self.edytuj_godziny_otwarcia(connection)
            elif choice == "5":
                break
            elif choice == "4":
                self.zarzadzaj_wyjątkami(connection)

    def ustaw_nowe_godziny_otwarcia(self, connection):
        if self.Moderator:
            try:
                cursor = connection.cursor()
                list = []
                list.append(self.Moderator)

                choice = input("Wszystkie obecne godziny otwarcia zostaną usunięte jeśli jesteś pewien,że chcesz"
                               " to zrobić wcisnij y ")
                if choice == 'y':
                    week = ["Poniedziałek", 'Wtorek', 'Sroda', 'Czwartek', 'Piatek', 'Sobota', 'Niedziela']
                    query = f"DELETE FROM Opening_Hours WHERE Salon_ID =%s"
                    cursor.execute(query, (list))
                    connection.commit()

                    for i in range(len(week)):
                        a, b = input(
                            f"Podaj godziny otwarcia dla {week[i]} w formacie xx:xx yy:yy, gdzie x oznacza godziny otwarcia"
                            " salonu"
                            " natomiast yy godziny zamkniecia salonu ").split()

                        # Dodanie pracownika
                        query = "INSERT INTO Opening_Hours (Salon_ID, Week_Day, Opening_Hour, Closing_Hour) VALUES (%s,%s,%s,%s)"
                        cursor.execute(query, (self.Moderator, week[i], a, b))
                        connection.commit()
                        print("Nowe godizny otwarcia została dodane do salonu.")
                    list.clear()
            except:
                print("Błąd podczas dodawania nowych godzin dla salonu, podałeś zły format dannych")
            finally:
                if cursor:
                    cursor.close()
        else:
            print("Nie masz uprawnień do dowania nowych pracowników.")

    def edytuj_godziny_otwarcia(self, connection):
        if self.Moderator:
            self.show_opening_hour(connection)
            week_day = input("Podaj dzień tygodnia który chcesz edytować: ")

            try:
                open, close = input(
                    f"Podaj nowe godziny otwarcia dla {week_day} w formacie xx:xx yy:yy, gdzie x oznacza godziny otwarcia"
                    " salonu"
                    " natomiast yy godziny zamkniecia salonu ").split()
                try:
                    cursor = connection.cursor()

                    query = f"UPDATE Opening_Hours SET Opening_Hour = %s, Closing_Hour = %s WHERE Salon_ID = %s AND Week_Day = %s"
                    cursor.execute(query, (open, close, self.Moderator, week_day))
                    connection.commit()
                    print("Dane godzin otwarcia zostały zaktualizowane.")
                except:
                    print("Błąd podczas aktualizacji godzin otwarcia:")
                finally:
                    if cursor:
                        cursor.close()
            except:
                print("Błąd podczas aktualizacji godzin otwarcia")
        else:
            print("Nie masz uprawnien do edycji tych danych")

    def show_exceptions(self, connection):
        cursor = connection.cursor()
        values = []
        values.append(self.Moderator)
        # Wykonywanie zapytania SQL
        query = f"SELECT Exceptions.Exception_ID,Exceptions.Opening_Hour, Exceptions.Closing_Hour, Exceptions.Starting_Date," \
                f" Exceptions.Ending_Date FROM Exceptions join Hair_Salon on (Hair_Salon.Salon_ID=Exceptions.Salon_ID)" \
                f" WHERE Hair_Salon.Salon_ID = %s"

        cursor.execute(query, values)

        # Pobieranie wyników
        records = cursor.fetchall()

        # Wyświetlenie wyników
        for row in records:
            total_seconds = int(row[1].total_seconds())

            # Obliczanie godzin i minut
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            # Formatowanie i wyświetlanie wyniku
            formatted_time1 = f"{hours}:{minutes:02d}"

            total_seconds = int(row[2].total_seconds())
            # Obliczanie godzin i minut
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            # Formatowanie i wyświetlanie wyniku
            formatted_time2 = f"{hours}:{minutes:02d}"
            print(f"ID: {row[0]} {row[3]} - {row[4]} \n{formatted_time1}-{formatted_time2}\n")

    def dodaj_wyjątek(self, connection):
        if self.Moderator:
            # week_day = input("Podaj dzień tygodnia który chcesz edytować: ")

            try:
                oh, ch, od, ed = input(
                    f"Podaj nowe godziny otwarcia oraz date w formacie xx:xx yy:yy rrrr-mm-dd rrrr-mm-dd, gdzie x"
                    f" oznacza godziny otwarcia salonu,\n"
                    "yy godziny zamkniecia salonu,"
                    "a r-m-d date początkową oraz końcowa wyjątku: ").split()
                try:
                    cursor = connection.cursor()

                    query = f"INSERT INTO Exceptions (Exceptions.Salon_ID, Exceptions.Opening_Hour," \
                            f" Exceptions.Closing_Hour, Exceptions.Starting_Date,Exceptions.Ending_Date)" \
                            f" VALUES (%s,%s,%s,%s,%s)"
                    cursor.execute(query, (self.Moderator,oh, ch, od, ed))
                    connection.commit()
                    print("Nowy wyjątek został dodany.")
                except:
                    print("Błąd podczas dodawnia wyjątku")
                finally:
                    if cursor:
                        cursor.close()
            except:
                print("Błąd podczas dodawnia wyjątku")
        else:
            print("Nie masz uprawnien do edycji tych danych")

    def usun_wyjątek(self, connection):
        if self.Moderator:
            self.show_exceptions(connection)
            worker_id=int(input("Podaj ID wyjątku który chcesz usunąć ze swojego salonu: "))
            try:
                cursor = connection.cursor()

                # Usunięcie pracownika
                query = "DELETE FROM Exceptions WHERE Salon_ID = %s AND Exception_ID = %s"
                cursor.execute(query, (int(self.Moderator), worker_id))
                connection.commit()
                print("Wyjątek został usunięty.")
            except Error as e:
                print("Błąd podczas usuwania wyjątku:", e)
            finally:
                if cursor:
                    cursor.close()
        else:
            print("Nie masz uprawnień do usuwania tych danych.")

class Report:
    def __init__(self, report_id, user_id, report_date, report_description):
        self.report_id = report_id
        self.user_id = user_id
        self.report_date = report_date
        self.report_description = report_description

class Opinion:
    def __init__(self, opinion_id, user_id, salon_id, stars, content):
        self.opinion_id = opinion_id
        self.user_id = user_id
        self.salon_id = salon_id
        self.stars = stars
        self.content = content

class LikedSalon:
    def __init__(self, liked_salon_id, user_id, salon_id):
        self.liked_salon_id = liked_salon_id
        self.user_id = user_id
        self.salon_id = salon_id

class HairSalon:
    def __init__(self, salon_id, name, address, owner, parking_lot, phone_no):
        self.salons =[]
        self.salon_id = salon_id
        self.name = name
        self.address = address
        self.owner = owner
        self.parking_lot = parking_lot
        self.phone_no = phone_no

class Worker:
    def __init__(self, worker_id, salon_id, name, surname, photo, description, moderator, hairdresser, password):
        self.worker_id = worker_id
        self.salon_id = salon_id
        self.name = name
        self.surname = surname
        self.photo = photo
        self.description = description
        self.moderator = moderator
        self.hairdresser = hairdresser
        self.password = password

class Exception:
    def __init__(self, exception_id, salon_id, opening_hour, closing_hour, start_date, end_date):
        self.exception_id = exception_id
        self.salon_id = salon_id
        self.opening_hour = opening_hour
        self.closing_hour = closing_hour
        self.start_date = start_date
        self.end_date = end_date

class OpeningHour:
    def __init__(self, id, salon_id, week_day, opening_hour, closing_hour):
        self.id = id
        self.salon_id = salon_id
        self.week_day = week_day
        self.opening_hour = opening_hour
        self.closing_hour = closing_hour

class Service:
    def __init__(self, service_id, salon_id, name, description, photo):
        self.service_id = service_id
        self.salon_id = salon_id
        self.name = name
        self.description = description
        self.photo = photo

class Price:
    def __init__(self, service_id, salon_id, price):
        self.service_id = service_id
        self.salon_id = salon_id
        self.price = price

class Detail:
    def __init__(self, detail_id, service_id, salon_id, time, price):
        self.detail_id = detail_id
        self.service_id = service_id
        self.salon_id = salon_id
        self.time = time
        self.price = price