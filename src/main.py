from src.data.sales_data import (
    generate_sales_data,
    save_sales_data,
    load_sales_data
)
from src.transform.sales_transform import transform_sales_data
from src.validation.sales_validation import validate_sales_data


def main() -> None:
    sales_df = generate_sales_data()

    save_sales_data(sales_df)

    loaded_sales_df = load_sales_data()
    transformed_sales_df = transform_sales_data(loaded_sales_df)

    validation_errors = validate_sales_data(transformed_sales_df)

    if validation_errors:
        print("Validation failed:")
        for error in validation_errors:
            print(f"- (error)")
        return

    print("Validation passed.")
    print(transformed_sales_df)



if __name__ == "__main__":
    main()
