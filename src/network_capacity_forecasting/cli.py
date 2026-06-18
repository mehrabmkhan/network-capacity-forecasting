from argparse import ArgumentParser
from pathlib import Path

from .data import load_utilization_data
from .model import load_model, save_model, train_forecast_model
from .report import build_report, forecast_links, write_report


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="capacity-forecast")
    subparsers = parser.add_subparsers(dest="command", required=True)

    train_parser = subparsers.add_parser("train", help="Train the capacity forecast model")
    train_parser.add_argument("--data", required=True)
    train_parser.add_argument("--model", required=True)

    report_parser = subparsers.add_parser("report", help="Create a capacity forecast report")
    report_parser.add_argument("--data", required=True)
    report_parser.add_argument("--model", required=True)
    report_parser.add_argument("--output", required=True)

    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.command == "train":
        frame = load_utilization_data(args.data)
        result = train_forecast_model(frame)
        save_model(args.model, result)
        print(f"MAE: {result.mae:.2f} RMSE: {result.rmse:.2f} MAPE: {result.mape:.2f}%")
        print(f"Saved model to {args.model}")
        return

    if args.command == "report":
        frame = load_utilization_data(args.data)
        model_payload = load_model(args.model)
        forecast = forecast_links(frame, model_payload)
        report = build_report(forecast, model_payload)
        write_report(args.output, report)
        print(f"Wrote report to {Path(args.output)}")


if __name__ == "__main__":
    main()
