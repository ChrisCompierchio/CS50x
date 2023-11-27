-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Find crime scene description
-- SELECT description FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28 AND street = Humphrey Street";

-- Find license plate of person present at littering
-- SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND minute = 36 AND hour = 16;

-- Get name of person with the above license plate
-- SELECT name FROM people WHERE license_plate = "X4G3938";

-- Get Alexis' passport number
-- SELECT passport_number FROM people WHERE name = "Alexis" AND license_plate = "X4G3938";
-- Passport Number = 5310124622

-- Get Alexis' flight_id and seat
-- SELECT flight_id, seat FROM passengers WHERE passport_number = 5310124622;
-- flight ID = 8, Seat = 6D
-- flight ID = 44, Seat = 8C

-- Get destination flight id of first flight
-- SELECT origin_airport_id, destination_airport_id FROM flights WHERE id = 8;
-- destination flight id = 2

-- Get destination flight id of first flight
-- SELECT origin_airport_id, destination_airport_id FROM flights WHERE id = 44;
-- destination flight id = 3

-- Get airport information from flights
-- SELECT * FROM airports WHERE id = 2;
-- PEK, Beijing Capital International Airport, Beijing

-- Get airport information from flights
-- SELECT * FROM airports WHERE id = 3;
-- LAX, Los Angeles International Airport, Los Angeles

-- Find info on Alexis
-- SELECT * FROM people WHERE passport_number = 5310124622;
-- id = 630782, phone_number = (814) 555-5180

-- Find Alexis' phone records
-- SELECT * FROM phone_calls WHERE caller = "(814) 555-5180" OR receiver = "(814) 555-5180";
-- (529) 555-7276, (579) 555-5030, (458) 555-836, (801) 555-9266, (910) 555-3251, (016) 555-9166

-- Get names of callers found in phone records
-- SELECT * FROM people WHERE phone_number = "(529) 555-7276" OR phone_number = "(579) 555-5030" OR phone_number = "(458) 555-836" OR phone_number = "(801) 555-9266" OR phone_number = "(910) 555-3251" OR phone_number = "(016) 555-9166";

-- DEAD END
-- START OVER

-- Get potential witnesses
-- SELECT * FROM interviews WHERE transcript LIKE "%bakery%";
-- Ruth: Car left 10 min after
-- Eugene: thief withdrew money at Leggett Street ATM
-- Raymond: thief called someone for less than a minute, took earliest flight out of fiftyville, other person purchased plane ticket.

-- Find earliest flight from airport
-- SELECT * FROM flights WHERE year = 2021 AND month = 7 AND day = 28 AND origin_airport_id = 8;

-- Find destination airports
-- SELECT * FROM airports WHERE id = 7 OR id = 5 OR id = 4;
-- Earliest flight went to Dallas with flight id = 6

-- Find people who flew to Dallas
-- SELECT * FROM passengers WHERE flight_id = 6;

-- Find people with these passport numbers
-- SELECT * FROM people WHERE passport_number = 3835860232 OR passport_number = 1618186613 OR passport_number = 7179245843 OR passport_number = 1682575122 OR passport_number = 7597790505 OR passport_number = 6128131458 OR passport_number = 6264773605 OR passport_number = 3642612721;

-- Find banking info of potential suspects
-- SELECT * FROM atm_transactions WHERE atm_location = "Leggett Street" AND transaction_type = "withdraw" AND month = 7 AND day = 28;

-- Check if bank accounts match any of the "witnesses"
-- SELECT * FROM bank_accounts WHERE account_number = 28500762 OR account_number = 28296815 OR account_number = 76054385 OR account_number = 49610011 OR account_number = 16153065 OR account_number = 25506511 OR account_number = 81061156 OR account_number = 26013199;

-- DEAD END
-- START OVER

-- Read crime report
-- SELECT * FROM crime_scene_reports WHERE month = 7 AND day = 28;

-- Narrow down interviews to inclue "bakery"
-- SELECT * FROM interviews WHERE transcript LIKE "%bakery%";

-- Look for cars that left within 10 min of the theft
-- SELECT license_plate, activity FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25;

-- Find people with these plates
-- SELECT * FROM people, bakery_security_logs WHERE people.license_plate = bakery_security_logs.license_plate AND bakery_security_logs.year = 2021 AND bakery_security_logs.month = 7 AND bakery_security_logs.day = 28 AND bakery_security_logs.hour = 10 AND bakery_security_logs.minute >= 15 AND bakery_security_logs.minute <= 25;

-- Find phone calls under 1 min and match phone numbers
-- SELECT * FROM phone_calls WHERE duration <= 60 AND month = 7 AND day = 28;

-- Luca and Bruce made phone calls under one minute and exited the bakery within the given time frame.
-- Luca got a call from Kathryn
-- Check if Kathryn flew out of the airport with ID 8 (found earlier)
-- SELECT * FROM passengers WHERE passport_number = 6121106406;
-- SELECT * FROM flights WHERE id = 34;
-- She flew from 8 to 5 (Dallas)
-- Check if she went to the bakery
-- SELECT * FROM bakery_security_logs WHERE license_plate = "4ZY7I8T";
-- She did NOT enter the bakery on that day, so we know Bruce is our thief!
-- Check who Bruce called
-- SELECT * FROM people WHERE phone_number = "(375) 555-8161";
-- BRUCE CALLED ROBIN!!!! SHE IS THE ACCOMPLICE
-- Check where Bruce flew to
-- SELECT flight_id FROM passengers WHERE passport_number = 5773159633;
-- SELECT destination_airport_id FROM flights WHERE id = 36;
-- SELECT city FROM airports WHERE id = 4;
-- HE FLEW TO NEW YORK CITY!!