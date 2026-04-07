#!/usr/bin/env python3
"""
Deploy script for Snowflake SQL deployments
Reads YAML deployment configurations and generates deployment manifests
"""

import sys
import os
import glob
from pathlib import Path
from datetime import datetime
import yaml


def get_config_dir(project_root: Path, environment: str, week: str = None) -> tuple:
    """Determine deployment config directory based on environment.

    Non-prod environments (dev, uat, preprod) use the same scripts from non-prod folder.
    Prod environment requires explicit week parameter and uses prod/{week} folder.
    """
    deployment_dir = project_root / "deployment"

    if environment == "prod":
        if not week:
            raise ValueError("Production deployment requires --week argument. Usage: python deploy.py prod <week>")

        config_dir = deployment_dir / "prod" / week
    else:
        # All non-prod environments (dev, uat, preprod) use the same non-prod folder
        config_dir = deployment_dir / "non-prod"

    if not config_dir.exists():
        raise FileNotFoundError(f"Deployment config directory not found: {config_dir}")

    return config_dir, week if environment == "prod" else None


def load_yaml_files(config_dir: Path) -> dict:
    """Load all YAML files from config directory."""
    yaml_files = sorted(config_dir.glob("*.yaml"))

    if not yaml_files:
        raise FileNotFoundError(f"No YAML files found in {config_dir}")

    all_scripts = []

    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r') as f:
                config = yaml.safe_load(f)

            if config and 'scripts' in config:
                scripts = config['scripts']
                if isinstance(scripts, list):
                    all_scripts.extend(scripts)
                else:
                    raise ValueError(f"'scripts' must be a list in {yaml_file}")
        except Exception as e:
            print(f"❌ Error reading {yaml_file}: {e}")
            sys.exit(1)

    return {
        'scripts': all_scripts,
        'yaml_count': len(yaml_files)
    }


def extract_sql_metadata(project_root: Path, script_path: str) -> dict:
    """Extract all metadata from SQL file header."""
    metadata = {
        'path': script_path,
        'jira_issue': 'N/A',
        'author': 'N/A',
        'impact': 'N/A',
    }

    try:
        full_path = project_root / script_path
        with open(full_path, 'r') as f:
            content = f.read(800)  # Read first 800 chars for metadata

            # Extract metadata from comments (simple line-by-line search)
            for line in content.split('\n'):
                if 'JIRA Issue:' in line:
                    metadata['jira_issue'] = line.split('JIRA Issue:')[1].strip()
                elif 'Author:' in line:
                    metadata['author'] = line.split('Author:')[1].strip()
                elif 'Impact:' in line:
                    metadata['impact'] = line.split('Impact:')[1].strip()

    except Exception as e:
        pass  # If we can't read metadata, use defaults

    return metadata


def generate_manifest(environment: str, scripts: list, week: str = None) -> str:
    """Generate deployment manifest content (script paths only)."""
    manifest = [
        "sampleprofile",
        "",
    ]

    manifest.extend(scripts)
    manifest.append("")  # Trailing newline

    return "\n".join(manifest)


def generate_overview(project_root: Path, environment: str, scripts: list, week: str = None) -> str:
    """Generate deployment overview with complete metadata for reviewers (Markdown format)."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    overview = [
        "# Deployment Overview",
        "",
        "## Deployment Information",
        "",
        f"- **Environment**: {environment}",
    ]

    if week:
        overview.append(f"- **Deployment Week**: {week}")

    overview.extend([
        f"- **Generated**: {timestamp}",
        f"- **Total Scripts**: {len(scripts)}",
        "",
        "## Deployment Scripts",
        "",
    ])

    for idx, script in enumerate(scripts, 1):
        metadata = extract_sql_metadata(project_root, script)

        overview.append(f"### {idx}. {script}")
        overview.append("")
        overview.append(f"**JIRA Issue**: {metadata['jira_issue']}")
        overview.append(f"**Author**: {metadata['author']}")
        overview.append(f"**Impact**: {metadata['impact']}")
        overview.append("")

    return "\n".join(overview)


def validate_scripts(project_root: Path, scripts: list) -> None:
    """Validate that all script files exist."""
    missing_files = []

    for script in scripts:
        script_path = project_root / script
        if not script_path.exists():
            missing_files.append(script)

    if missing_files:
        print(f"❌ Error: {len(missing_files)} script file(s) not found:")
        for script in missing_files:
            print(f"   - {script}")
        sys.exit(1)


def main():
    """Main deployment function."""
    if len(sys.argv) < 2:
        print("Usage: python deploy.py <environment> [week]")
        print()
        print("Environments: dev, uat, preprod, prod")
        print("  - dev, uat, preprod: Deploy to non-prod (same scripts for all)")
        print("  - prod: Deploy to production (requires week argument)")
        print()
        print("Examples:")
        print("  python deploy.py dev")
        print("  python deploy.py uat")
        print("  python deploy.py preprod")
        print("  python deploy.py prod 2026-w15")
        print("  python deploy.py prod 2026-w16")
        sys.exit(1)

    environment = sys.argv[1]
    week = sys.argv[2] if len(sys.argv) > 2 else None

    # Validate environment
    valid_environments = ["dev", "uat", "preprod", "prod"]
    if environment not in valid_environments:
        print(f"❌ Error: Invalid environment. Must be one of: {', '.join(valid_environments)}")
        sys.exit(1)

    # Resolve project root (directory containing this script)
    project_root = Path(__file__).resolve().parent

    try:
        # Get config directory
        config_dir, prod_week = get_config_dir(project_root, environment, week)

        # Load YAML files
        config_data = load_yaml_files(config_dir)
        scripts = config_data['scripts']

        # Validate scripts exist
        validate_scripts(project_root, scripts)

        # Generate manifest and overview
        manifest = generate_manifest(environment, scripts, prod_week)
        overview = generate_overview(project_root, environment, scripts, prod_week)

        # Write artifact files
        scripts_dir = project_root / "scripts"
        manifest_file = scripts_dir / "2_scripts"
        overview_file = project_root / "deploy_overview.md"

        with open(manifest_file, 'w') as f:
            f.write(manifest)

        with open(overview_file, 'w') as f:
            f.write(overview)

        # Display overview
        print(overview)

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
