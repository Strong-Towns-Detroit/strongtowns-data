"""Internal maintainer entry point. Never invoked by the public BZA CLI."""

import argparse
import json
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build")
    build.add_argument("--source", type=Path, required=True)
    build.add_argument("--output", type=Path, required=True)
    build.add_argument("--reviews", type=Path, required=True)
    build.add_argument("--parcels", type=Path)
    build.add_argument("--addresses", type=Path)
    package = commands.add_parser("package")
    package.add_argument("--source", type=Path, required=True)
    package.add_argument("--output", type=Path, required=True)
    package.add_argument("--version", required=True)
    package.add_argument("--release-url", required=True)
    package.add_argument("--prior-index", type=Path)
    for name in ("minutes", "extract", "project-types", "intake"):
        command = commands.add_parser(name)
        command.add_argument("--output", type=Path, required=True)
        command.add_argument("--apply", action="store_true")
        if name != "minutes":
            command.add_argument("--source", type=Path, required=True)
        if name in ("extract", "project-types"):
            command.add_argument("--allow-paid", action="store_true")
            command.add_argument("--model")
            command.add_argument("--limit", type=int, default=1)
            command.add_argument("--all", action="store_true")
            command.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    from dotenv import load_dotenv

    load_dotenv(Path.cwd() / ".env")
    if args.command == "build":
        from .build import build

        build(
            args.source,
            args.output,
            reviews=args.reviews,
            parcels=args.parcels,
            addresses=args.addresses,
        )
    elif args.command == "package":
        from .build import package

        prior = (
            json.loads(args.prior_index.read_text())["releases"]
            if args.prior_index
            else ()
        )
        print(
            package(
                args.source,
                args.output,
                version=args.version,
                release_url=args.release_url,
                prior_releases=prior,
            )
        )
    elif args.command == "minutes":
        from .minutes import download_bza_minutes

        print(json.dumps(download_bza_minutes(args.output, apply=args.apply), indent=2))
    elif args.command in ("extract", "project-types"):
        options = dict(
            output_dir=args.output,
            model=args.model,
            limit=args.limit,
            all=args.all,
            force=args.force,
            dry_run=not args.apply,
            allow_paid=args.allow_paid,
        )
        if args.command == "extract":
            from .extract_bza_with_gemini import run

            return run(pdf_dir=args.source, **options)
        from .classify_bza_project_types_with_gemini import run

        return run(histories_path=args.source, **options)
    else:
        from .enrich_bza_intake_dates import run

        return run(
            input_path=args.source,
            output=args.output / "intake_date_candidates.csv",
            raw_dir=args.output / "accela_raw",
            dry_run=not args.apply,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
