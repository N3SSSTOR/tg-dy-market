from utils.profile_img import generate_profile_img


def test() -> None:
    res = generate_profile_img(
        username="@N3SSTORR",
        days_in_market=3,
        total_purchases=4,
        total_amount=10000
    )    
    print(res)


if __name__ == "__main__":
    test()