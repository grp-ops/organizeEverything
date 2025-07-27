#!/usr/bin/env python3

import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional


class ProjectBuilder:
    def __init__(self, templates_file: str = "templates.json"):
        self.templates_file = Path(templates_file)
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load project templates from JSON file"""
        try:
            with open(self.templates_file, 'r') as f:
                data = json.load(f)
                return data.get('templates', {})
        except FileNotFoundError:
            print(f"Templates file '{self.templates_file}' not found")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error parsing templates file: {e}")
            return {}
    
    def list_templates(self) -> None:
        """List available project templates"""
        if not self.templates:
            print("No templates available")
            return
        
        print("Available templates:")
        for key, template in self.templates.items():
            name = template.get('name', key)
            description = template.get('description', 'No description')
            print(f"  {key}: {name} - {description}")
    
    def create_project(self, template_name: str, project_name: str, 
                      destination: Optional[str] = None) -> bool:
        """Create a project using the specified template"""
        if template_name not in self.templates:
            print(f"Template '{template_name}' not found")
            return False
        
        template = self.templates[template_name]
        
        # Set destination path
        if destination:
            base_path = Path(destination) / project_name
        else:
            base_path = Path.cwd() / project_name
        
        try:
            # Create base project directory
            base_path.mkdir(parents=True, exist_ok=True)
            
            # Create folders
            folders = template.get('folders', [])
            for folder in folders:
                folder_path = base_path / folder
                folder_path.mkdir(parents=True, exist_ok=True)
            
            # Create files
            files = template.get('files', [])
            for file_info in files:
                file_path = base_path / file_info['path']
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(file_path, 'w') as f:
                    f.write(file_info.get('content', ''))
            
            print(f"Project '{project_name}' created successfully at: {base_path}")
            return True
            
        except Exception as e:
            print(f"Error creating project: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="Create project directory structures from templates")
    parser.add_argument('command', choices=['list', 'create'], 
                       help='Command to execute')
    parser.add_argument('-t', '--template', 
                       help='Template name to use for project creation')
    parser.add_argument('-n', '--name', 
                       help='Project name')
    parser.add_argument('-d', '--destination', 
                       help='Destination directory (defaults to current directory)')
    parser.add_argument('--templates-file', default='templates.json',
                       help='Path to templates JSON file')
    
    args = parser.parse_args()
    
    builder = ProjectBuilder(args.templates_file)
    
    if args.command == 'list':
        builder.list_templates()
    elif args.command == 'create':
        if not args.template:
            print("Error: Template name required for create command")
            return 1
        if not args.name:
            print("Error: Project name required for create command")
            return 1
        
        success = builder.create_project(args.template, args.name, args.destination)
        return 0 if success else 1


if __name__ == "__main__":
    exit(main())
