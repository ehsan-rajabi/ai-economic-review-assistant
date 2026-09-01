from django.shortcuts import render, HttpResponse
from ai_review import review_assumptions

def home(request):
    d = {}

    if request.method == "POST":

        discount_rate = request.POST.get("discount_rate")
        rate_wage_increase = request.POST.get("rate_wage_increase")
        rate_annuity_increase = request.POST.get("rate_annuity_increase")
        productivity_rate = request.POST.get("productivity_rate")
        male_retirement_age = request.POST.get("male_retirement_age")
        female_retirement_age = request.POST.get("female_retirement_age")
        male_retiement_service = request.POST.get("male_retiement_service")
        female_retirement_service = request.POST.get("female_retirement_service")
        max_service_years = request.POST.get("max_service_years")
        permium_rate_employer = request.POST.get("permium_rate_employer")
        permium_rate_employee = request.POST.get("permium_rate_employee")
        interst_rate = request.POST.get("interst_rate")
        borrowing_rate = request.POST.get("borrowing_rate")
        d.update({
       "discount_rate": discount_rate,
       "rate_wage_increase": rate_wage_increase,
       "rate_annuity_increase": rate_annuity_increase,
       "productivity_rate": productivity_rate,
       "male_retirement_age": male_retirement_age,
       "female_retirement_age": female_retirement_age,
       "male_retiement_service": male_retiement_service,
       "female_retirement_service": female_retirement_service,
       "max_service_years": max_service_years,
       "permium_rate_employer": permium_rate_employer,
       "permium_rate_employee": permium_rate_employee,
       "interst_rate": interst_rate,
       "borrowing_rate": borrowing_rate,
})
        # 1. Check if any requirement is missing
        if (
            not discount_rate
            or not rate_wage_increase
            or not rate_annuity_increase
            or not productivity_rate
            or not male_retirement_age
            or not female_retirement_age
            or not male_retiement_service
            or not female_retirement_service
            or not max_service_years
            or not permium_rate_employer
            or not permium_rate_employee
            or not interst_rate
            or not borrowing_rate
        ):
            d["response"] = "Please insert all requirements."
            return render(request, "mainapp/index.html", context=d)

        # 2. Convert strings to numbers
        discount_rate = float(discount_rate)
        rate_wage_increase = float(rate_wage_increase)
        rate_annuity_increase = float(rate_annuity_increase)
        productivity_rate = float(productivity_rate)
        male_retirement_age = float(male_retirement_age)
        female_retirement_age = float(female_retirement_age)
        male_retiement_service = float(male_retiement_service)
        female_retirement_service = float(female_retirement_service)
        max_service_years = float(max_service_years)
        permium_rate_employer = float(permium_rate_employer)
        permium_rate_employee = float(permium_rate_employee)
        interst_rate = float(interst_rate)
        borrowing_rate = float(borrowing_rate)

        # 3. Check positive numbers
        values = {
            "Discount rate": discount_rate,
            "Wage increase": rate_wage_increase,
            "Annuity increase": rate_annuity_increase,
            "Productivity rate": productivity_rate,
            "Male retirement age": male_retirement_age,
            "Female retirement age": female_retirement_age,
            "Male retirement service": male_retiement_service,
            "Female retirement service": female_retirement_service,
            "Maximum service years": max_service_years,
            "Employer premium rate": permium_rate_employer,
            "Employee premium rate": permium_rate_employee,
            "Interest rate": interst_rate,
            "Borrowing rate": borrowing_rate,
        }

        for name, value in values.items():
            if value <= 0:
                d["response"] = f"{name} should be positive."
                return render(
                    request,
                    "mainapp/index.html",
                    context=d
                )

        # 4. Check retirement age
        if male_retirement_age <= 55:
            d["response"] = "Male retirement age should be bigger than 55."
            return render(request, "mainapp/index.html", context=d)

        if female_retirement_age <= 55:
            d["response"] = "Female retirement age should be bigger than 55."
            return render(request, "mainapp/index.html", context=d)
        if max_service_years < male_retiement_service or max_service_years<female_retirement_service :
                    d["response"] = "max_service_years should be bigger than male_retiement_service and female_retirement_service."
                    return render(request, "mainapp/index.html", context=d)
        # 5. Everything is valid
        d["response"] = "You submitted the requirements successfully."
        # Send the six economic assumptions to OpenAI
        ai_result = review_assumptions(discount_rate,rate_wage_increase,rate_annuity_increase,productivity_rate,interst_rate,borrowing_rate,)
        d["ai_score"] = ai_result["score"]
        d["ai_review"] = ai_result["review"]
        d["ai_suggestions"] = ai_result["suggestions"]
    return render(request, "mainapp/index.html", context=d)


def contact(request):
    return render(request, "mainapp/contact.html")


def introduction(request):
    return HttpResponse("this is app for prediction of trends")
