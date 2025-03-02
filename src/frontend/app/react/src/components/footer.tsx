import { Github } from "lucide-react";

interface Translation {
  termsOfService: string;
  privacy: string;
}

export default function Footer({ t }: { t: Translation }) {
  return (
    <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6 border-t">
      <div className="flex items-center gap-2">
        <a
          href="https://github.com/DailyDevQ"
          target="_blank"
          rel="noopener noreferrer"
          className="text-gray-500 hover:text-gray-700 transition-colors"
        >
          <Github className="h-5 w-5" />
        </a>
        <p className="text-xs text-gray-500">© 2024 DailyDevQ. All rights reserved.</p>
      </div>
      <nav className="sm:ml-auto flex gap-4 sm:gap-6">
        <a className="text-xs hover:underline underline-offset-4" href="#">
          {t.termsOfService}
        </a>
        <a className="text-xs hover:underline underline-offset-4" href="#">
          {t.privacy}
        </a>
      </nav>
    </footer>
  );
}
