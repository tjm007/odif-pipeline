from src.data.sales_data import (
    generate_sales_data,
    save_sales_data,
    load_sales_data
)


def main() -> None:
    sales_df = generate_sales_data()

    save_sales_data(sales_df)

    loaded_sales_df = load_sales_data()

    print(loaded_sales_df)

if __name__ == "__main__":
    main()
