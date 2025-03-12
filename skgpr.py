import random
import string
import os
import time

try:
    from google_play_scraper import app, exceptions
except ModuleNotFoundError:
    os.system('pip install google_play_scraper')

def generate_code():
    # Google Play redemption codes typically consist of 16 characters,
    # where the first 4 characters are uppercase letters and the remaining
    # characters are alphanumeric (uppercase letters and digits).
    code = ''.join(random.choices(string.ascii_uppercase, k=4))
    code += ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    return code

def check_redeemability(codes, country="us"):
    redeemable_codes = []
    try:
        for code in codes:
            try:
                result = app(code, lang="en", country=country)
                if result.get("url"):
                    redeemable_codes.append({"code": code, "url": result["url"]})
            except exceptions.NotFoundError:
                pass  # Code not found, ignore
            except exceptions.ExtraHTTPError:
                print(f"An HTTP error occurred while checking code {code}.")
            time.sleep(0.1)  # Add a small delay between requests to avoid rate limiting
    except Exception as e:
        print(f"An error occurred: {e}")
    return redeemable_codes

def main():
    num_codes_to_generate = 100  # Adjust the number of codes to generate
    codes_to_check = [generate_code() for _ in range(num_codes_to_generate)]
    country = "in"  # India
    redeemable_codes_list = check_redeemability(codes_to_check, country)

    print("Generated Codes:")
    for i, generated_code in enumerate(codes_to_check, start=1):
        print(f"{i}. {generated_code}")

    print("\nRedeemable Codes:")
    for redeemable_code in redeemable_codes_list:
        print(f"Code: {redeemable_code['code']}, URL: {redeemable_code['url']}")

    accuracy = len(redeemable_codes_list) / len(codes_to_check) * 100
    print(f"\nAccuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    print("Google Play Redemption Code Checker")
    print("Made by siwamking1")
    print("----------------------------------\n")
    main()
