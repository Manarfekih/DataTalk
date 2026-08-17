from __future__ import annotations

import pandas as pd
import streamlit as st


def render_table(rows):

    st.subheader("Returned Data")

    if not rows:

        st.info("No rows returned.")

        return

    df = pd.DataFrame(rows)

    st.write(f"Rows returned : {len(df)}")

    st.dataframe(

        df,

        width="stretch",

    )

    csv = df.to_csv(index=False)

    st.download_button(

        "⬇ Download CSV",

        csv,

        file_name="results.csv",

        mime="text/csv",

    )
