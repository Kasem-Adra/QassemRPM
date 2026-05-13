import argparse
import sys
import os
from qassemrpm.builder import build_spec
from qassemrpm.validator import validate_spec  # استيراد دالة التحقق الجديدة

def main():
    # 1. إعداد المعالج الأساسي
    parser = argparse.ArgumentParser(
        description="QassemRPM: A modern RPM packaging tool for developers."
    )
    
    # 2. إضافة الأوامر الفرعية (Sub-commands)
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # إعداد أمر البناء (build)
    build_parser = subparsers.add_parser("build", help="Build an RPM from a SPEC file")
    build_parser.add_argument("spec", help="Path to the .spec file (e.g., examples/hello.spec)")
    build_parser.add_argument("--workdir", help="Custom workspace directory (_topdir)", default=None)

    # إعداد أمر التحقق (spec validate) - المهمة رقم 8
    spec_parser = subparsers.add_parser("spec", help="SPEC file utilities")
    spec_subparsers = spec_parser.add_subparsers(dest="spec_command")
    
    validate_parser = spec_subparsers.add_parser("validate", help="Validate a SPEC file tags")
    validate_parser.add_argument("path", help="Path to the .spec file")

    args = parser.parse_args()

    # 3. معالجة الأوامر
    
    # تنفيذ أمر البناء (build)
    if args.command == "build":
        if not os.path.exists(args.spec):
            print(f"\033[91m❌ Error: File '{args.spec}' not found.\033[0m")
            sys.exit(1)

        print(f"\033[94m🛠️  Building RPM for: {args.spec}...\033[0m")
        success, output = build_spec(args.spec, topdir=args.workdir)
        
        if success:
            print("\033[92m✅ Build completed successfully!\033[0m")
            print("\033[90m" + "-"*30 + " LOGS " + "-"*30 + "\033[0m")
            print(output)
        else:
            print("\033[91m🛑 Build failed! Check the logs below:\033[0m")
            print("\033[90m" + "-"*30 + " ERROR " + "-"*30 + "\033[0m")
            print(output)
            sys.exit(1)

    # تنفيذ أمر التحقق (spec validate)
    elif args.command == "spec" and args.spec_command == "validate":
        print(f"\033[94m🔍 Validating SPEC file: {args.path}...\033[0m")
        success, message = validate_spec(args.path)
        
        if success:
            print(f"\033[92m✅ {message}\033[0m")
        else:
            print(f"\033[91m❌ Validation Error: {message}\033[0m")
            sys.exit(1)

    else:
        # عرض المساعدة إذا لم يتم إدخال أمر أو إذا كان الأمر ناقصاً
        parser.print_help()

if __name__ == "__main__":
    main()
