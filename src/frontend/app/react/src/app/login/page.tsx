"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import Link from "next/link"
import { Github, Mail, MessageCircle, Globe, Facebook, Apple } from "lucide-react"
import { content } from "@/constants/content"

export default function LoginPage() {
  const [language, setLanguage] = useState("kr")
  const t = content[language]

  return (
    <div className="flex items-center justify-center min-h-screen bg-white dark:bg-gray-900">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle className="text-2xl text-center">{t.login}</CardTitle>
          <CardDescription className="text-center">Choose your preferred login method</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            <Button variant="outline" className="w-full">
              <Github className="mr-2 h-4 w-4" />
              Continue with GitHub
            </Button>
            <Button variant="outline" className="w-full bg-[#FEE500] text-black hover:bg-[#FEE500]/90">
              <MessageCircle className="mr-2 h-4 w-4" />
              Continue with Kakao
            </Button>
            <Button variant="outline" className="w-full bg-[#03C75A] text-white hover:bg-[#03C75A]/90">
              <Globe className="mr-2 h-4 w-4" />
              Continue with Naver
            </Button>
            <Button variant="outline" className="w-full bg-[#4285F4] text-white hover:bg-[#4285F4]/90">
              <Mail className="mr-2 h-4 w-4" />
              Continue with Google
            </Button>
            <Button variant="outline" className="w-full bg-[#1877F2] text-white hover:bg-[#1877F2]/90">
              <Facebook className="mr-2 h-4 w-4" />
              Continue with Meta
            </Button>
            <Button variant="outline" className="w-full bg-black text-white hover:bg-black/90">
              <Apple className="mr-2 h-4 w-4" />
              Continue with Apple
            </Button>
          </div>
          <div className="mt-6 text-center text-sm">
            <Link href="/" className="text-purple-600 hover:underline">
              {language === "kr" ? "홈으로 돌아가기" : "Back to Home"}
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

