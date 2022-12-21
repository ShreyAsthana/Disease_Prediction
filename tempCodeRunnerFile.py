
        print(dict)
        # print(predictDisease("Itching,Skin Rash,Nodal Skin Eruptions,Dischromic  Patches"))
        print(predictDisease(f"{','.join(dict.getlist('Symptoms'))}"))

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
