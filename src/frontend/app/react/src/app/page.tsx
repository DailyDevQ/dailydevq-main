    "use client"

    import { useState, useEffect } from "react"
    import { Button } from "@/components/ui/button"
    import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
    import { CheckCircle, Code, Zap, ChevronUp } from "lucide-react"
    import Link from "next/link"
    import Header from "@/components/header"
    import Footer from "@/components/footer"
    import { ThemeToggle } from "@/components/theme-toggle"
    import { useScrollToTop } from "@/utils/scroll"
    import { content } from "@/constants/content"

    export default function Home() {
    const [mounted, setMounted] = useState(false)
    const [language, setLanguage] = useState("kr")
    const [showScrollTop, setShowScrollTop] = useState(false)
    const scrollToTop = useScrollToTop()

    useEffect(() => {
        setMounted(true)
        const handleScroll = () => {
        setShowScrollTop(window.pageYOffset > 300)
        }
        window.addEventListener("scroll", handleScroll)
        return () => window.removeEventListener("scroll", handleScroll)
    }, [])

    if (!mounted) return null

    const toggleLanguage = () => {
        setLanguage(language === "kr" ? "us" : "kr")
    }

    const t = content[language]

    return (
        <div className="flex flex-col min-h-screen">
        <Header t={t} language={language} toggleLanguage={toggleLanguage} />
        <main className="flex-1">
            <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48 bg-purple-50 dark:bg-purple-900">
            <div className="container px-4 md:px-6">
                <div className="flex flex-col items-center space-y-4 text-center">
                <div className="space-y-2">
                    <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none">
                    {t.title}
                    </h1>
                    <p className="mx-auto max-w-[700px] text-gray-500 md:text-xl dark:text-gray-400">{t.description}</p>
                </div>
                <div className="space-x-4">
                    <Link href="/login">
                    <Button className="bg-purple-600 text-white">{t.getStarted}</Button>
                    </Link>
                    <Button variant="outline">{t.learnMore}</Button>
                </div>
                </div>
            </div>
            </section>
            <section className="w-full py-12 md:py-24 lg:py-32 bg-white dark:bg-gray-800">
            <div className="container px-4 md:px-6">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl text-center mb-8">
                {t.features}
                </h2>
                <div className="grid gap-6 lg:grid-cols-3 lg:gap-12">
                <Card>
                    <CardHeader>
                    <Zap className="w-8 h-8 text-purple-600" />
                    <CardTitle>{t.aiQuestions}</CardTitle>
                    </CardHeader>
                    <CardContent>
                    <CardDescription>{t.aiQuestionsDesc}</CardDescription>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader>
                    <Code className="w-8 h-8 text-purple-600" />
                    <CardTitle>{t.multipleLanguages}</CardTitle>
                    </CardHeader>
                    <CardContent>
                    <CardDescription>{t.multipleLanguagesDesc}</CardDescription>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader>
                    <CheckCircle className="w-8 h-8 text-purple-600" />
                    <CardTitle>{t.progressTracking}</CardTitle>
                    </CardHeader>
                    <CardContent>
                    <CardDescription>{t.progressTrackingDesc}</CardDescription>
                    </CardContent>
                </Card>
                </div>
            </div>
            </section>
            <section className="w-full py-12 md:py-24 lg:py-32 bg-white dark:bg-gray-800">
            <div className="container px-4 md:px-6">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl text-center mb-8">
                {t.testimonials}
                </h2>
                <div className="grid gap-6 lg:grid-cols-3 lg:gap-12">
                <Card>
                    <CardContent className="pt-4">
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                        "DailyDevQ has been a game-changer in my interview prep. The AI-generated questions are spot-on and
                        have significantly improved my confidence."
                    </p>
                    <p className="mt-2 font-bold">- Sarah K., Software Engineer</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="pt-4">
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                        "I love how the questions adapt to my skill level. It's like having a personal interview coach!"
                    </p>
                    <p className="mt-2 font-bold">- Alex M., Frontend Developer</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="pt-4">
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                        "The variety of programming languages and topics covered is impressive. DailyDevQ has become an
                        essential part of my daily routine."
                    </p>
                    <p className="mt-2 font-bold">- Chris L., Full Stack Developer</p>
                    </CardContent>
                </Card>
                </div>
            </div>
            </section>
            <section className="w-full py-12 md:py-24 lg:py-32 bg-purple-50 dark:bg-purple-900">
            <div className="container px-4 md:px-6">
                <div className="flex flex-col items-center space-y-4 text-center">
                <div className="space-y-2">
                    <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">{t.readyToAce}</h2>
                    <p className="mx-auto max-w-[700px] text-gray-500 md:text-xl dark:text-gray-400">{t.joinThousands}</p>
                </div>
                <div className="space-x-4">
                    <Link href="/login">
                    <Button className="bg-purple-600 text-white">{t.getStartedNow}</Button>
                    </Link>
                </div>
                </div>
            </div>
            </section>
        </main>
        <Footer t={t} />
        <div className="fixed bottom-4 right-4 space-y-2">
            <ThemeToggle />
            {showScrollTop && (
            <Button variant="outline" size="icon" className="rounded-full" onClick={scrollToTop}>
                <ChevronUp className="h-[1.2rem] w-[1.2rem]" />
            </Button>
            )}
        </div>
        </div>
    )
    }

