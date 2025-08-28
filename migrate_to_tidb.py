{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "7d87b1cf-fac2-4574-9066-9edb6f49f7ac",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Copying city_scenarios_all...\n",
      "city_scenarios_all copied successfully!\n",
      "Copying dh_toilets...\n",
      "dh_toilets copied successfully!\n",
      "Copying dh_seniors...\n",
      "dh_seniors copied successfully!\n",
      "All tables copied to TiDB Cloud!\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "from sqlalchemy import create_engine\n",
    "\n",
    "# ----- Local MySQL -----\n",
    "local_user = \"root\"\n",
    "local_password = \"Rabarb3R\"\n",
    "local_db = \"final_project\"\n",
    "local_conn_str = f\"mysql+pymysql://{local_user}:{local_password}@localhost/{local_db}\"\n",
    "local_engine = create_engine(local_conn_str)\n",
    "\n",
    "# ----- TiDB Cloud -----\n",
    "tidb_user = \"2sb6DPBbimoR6v1.root\"\n",
    "tidb_password = \"80RMOEXPPOdIpIKi\"\n",
    "tidb_host = \"gateway01.eu-central-1.prod.aws.tidbcloud.com:4000\"\n",
    "tidb_db = \"test\"\n",
    "tidb_conn_str = (\n",
    "    f\"mysql+pymysql://{tidb_user}:{tidb_password}@{tidb_host}/{tidb_db}\"\n",
    "    \"?ssl_verify_cert=true&ssl_verify_identity=true\"\n",
    ")\n",
    "tidb_engine = create_engine(tidb_conn_str)\n",
    "\n",
    "# ----- Tables to copy -----\n",
    "tables = [\"city_scenarios_all\", \"dh_toilets\", \"dh_seniors\"]\n",
    "\n",
    "for table in tables:\n",
    "    print(f\"Copying {table}...\")\n",
    "    df = pd.read_sql(f\"SELECT * FROM {table}\", con=local_engine)\n",
    "    df.to_sql(table, con=tidb_engine, index=False, if_exists='replace')\n",
    "    print(f\"{table} copied successfully!\")\n",
    "\n",
    "print(\"All tables copied to TiDB Cloud!\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "5d45703a-478c-438f-bae9-22c0f3d5d18c",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Tables in TiDB Cloud: [('city_scenarios_all',), ('dh_seniors',), ('dh_toilets',)]\n"
     ]
    }
   ],
   "source": [
    "from sqlalchemy import create_engine, text\n",
    "\n",
    "tidb_user = \"2sb6DPBbimoR6v1.root\"\n",
    "tidb_password = \"80RMOEXPPOdIpIKi\"\n",
    "tidb_host = \"gateway01.eu-central-1.prod.aws.tidbcloud.com:4000\"\n",
    "tidb_db = \"test\"\n",
    "\n",
    "tidb_conn_str = (\n",
    "    f\"mysql+pymysql://{tidb_user}:{tidb_password}@{tidb_host}/{tidb_db}\"\n",
    "    \"?ssl_verify_cert=true&ssl_verify_identity=true\"\n",
    ")\n",
    "engine = create_engine(tidb_conn_str)\n",
    "\n",
    "with engine.connect() as conn:\n",
    "    tables = conn.execute(text(\"SHOW TABLES;\")).fetchall()\n",
    "    print(\"Tables in TiDB Cloud:\", tables)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ef411b23-8a99-4c9d-808c-044267ac7e18",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
