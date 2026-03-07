--IPO 
CREATE TABLE IPO (
	IPO_id BIGSERIAL PRIMARY KEY,
	IPO_code VARCHAR(50) UNIQUE NOT NULL,
	order_for TEXT NOT NULL,
	buyer_code  TEXT NOT NULL,
	program_name TEXT NOT NULL
);

--BUYERS TABLE
CREATE TABLE buyers (
    buyer_id           BIGSERIAL PRIMARY KEY,
    buyer_code         VARCHAR(50) UNIQUE NOT NULL,
    buyer_name         VARCHAR(50) NOT NULL,
    customer_name      VARCHAR(50) NOT NULL,
    contact_person     VARCHAR(50) NOT NULL,
    created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--VENDORS TABLE
CREATE TABLE vendors (
    vendor_id                BIGSERIAL PRIMARY KEY,
    vendor_code              VARCHAR(50) UNIQUE NOT NULL,
    vendor_name              VARCHAR(255) NOT NULL,
    gst_number               VARCHAR(20) NOT NULL,
    address                  TEXT NOT NULL,
    bank_name                VARCHAR(50) NOT NULL,
    account_number           VARCHAR(50) NOT NULL,
    ifsc_code                VARCHAR(20) NOT NULL,
    job_work_category        VARCHAR(100) NOT NULL,
    job_work_subcategory     VARCHAR(100) NOT NULL,
    contact_person           VARCHAR(50) NOT NULL,
    email                    VARCHAR(50) NOT NULL,
    whatsapp_number          VARCHAR(14) NOT NULL,
    alternate_whatsapp       VARCHAR(14),
    payment_terms            TEXT NOT NULL,
    created_at               TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Code Creation tables
--Company Essentials

--Electricals
CREATE TABLE electricals_ui (
    id SERIAL PRIMARY KEY,
    entry_date DATE NOT NULL,

    sr_no INT NOT NULL,
    item_description TEXT NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,

    unit VARCHAR(20) NOT NULL CHECK (
        unit IN ('METER', 'KGS', 'PCS', 'LITRE')
    ),

    remarks TEXT,
    reference_image VARCHAR(255),  -- store image path or URL

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Audit and compliance
CREATE TABLE audit_compliance_ui (
    id SERIAL PRIMARY KEY,
    entry_date DATE NOT NULL,

    sr_no INT NOT NULL,
    item_description TEXT NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,

    unit VARCHAR(20) NOT NULL CHECK (
        unit IN ('METER', 'KGS', 'PCS', 'LITRE')
    ),

    remarks TEXT,
    reference_image VARCHAR(255),  -- stores uploaded image path or URL

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Maintenance
CREATE TABLE maintenance_ui (
    id SERIAL PRIMARY KEY,
    entry_date DATE NOT NULL,

    sr_no INT NOT NULL,
    job_work TEXT NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,

    unit VARCHAR(20) NOT NULL CHECK (
        unit IN ('METER', 'KGS', 'PCS', 'LITRE')
    ),

    remarks TEXT,
    reference_image VARCHAR(255),   -- stores uploaded image path or URL

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Repair
CREATE TABLE repair_ui (
    id SERIAL PRIMARY KEY,
    entry_date DATE NOT NULL,

    sr_no INT NOT NULL,
    job_work TEXT NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,

    unit VARCHAR(20) NOT NULL CHECK (
        unit IN ('METER', 'KGS', 'PCS', 'LITRE')
    ),

    remarks TEXT,
    reference_image VARCHAR(255),   -- stores uploaded image path or URL

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Hardware and chemicals
CREATE TABLE hardware_chemicals_ui (
    id SERIAL PRIMARY KEY,
    entry_date DATE NOT NULL,

    sr_no INT NOT NULL,
    item_description TEXT NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,

    unit VARCHAR(20) NOT NULL CHECK (
        unit IN ('METER', 'KGS', 'PCS', 'LITRE')
    ),

    remarks TEXT,
    reference_image VARCHAR(255),   -- stores uploaded image path or URL

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Machinery
CREATE TABLE machinery_ui (
    id SERIAL PRIMARY KEY,

    sr_no INT NOT NULL,
    machine_type VARCHAR(100) NOT NULL,
    component_spec TEXT NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,

    unit VARCHAR(20) NOT NULL CHECK (
        unit IN ('METER', 'KGS', 'PCS', 'LITRE')
    ),

    remarks TEXT,

    department VARCHAR(50) NOT NULL CHECK (
        department IN (
            'BRAIDING',
            'CARPET',
            'CUTTING',
            'DYEING',
            'EMBROIDERY',
            'KNITTING',
            'PRINTING',
            'QUILTING',
            'SEWING',
            'TUFTING',
            'WEAVING'
        )
    ),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Travel Expense
CREATE TABLE travel_expense_ui (
    id SERIAL PRIMARY KEY,
    entry_date DATE NOT NULL,

    sr_no INT NOT NULL,
    item_description VARCHAR(100) NOT NULL CHECK (
        item_description IN ('HOTEL STAY', 'FUEL-PETROL', 'FOOD EXPENSE')
    ),

    amount DECIMAL(12,2) NOT NULL,

    remarks TEXT,
    expense_for VARCHAR(150) NOT NULL,   -- corresponds to "FOR" column

    reference_image VARCHAR(255),         -- uploaded bill/receipt image path or URL

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Stationary
CREATE TABLE stationary_ui (
    id SERIAL PRIMARY KEY,
    entry_date DATE NOT NULL,

    sr_no INT NOT NULL,
    item_description TEXT NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,

    unit VARCHAR(20) NOT NULL CHECK (
        unit IN ('METER', 'KGS', 'PCS', 'LITRE')
    ),

    remarks TEXT,
    reference_image VARCHAR(255),   -- stores uploaded image path or URL

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--QC Tools
CREATE TABLE qc_tools_ui (
    id SERIAL PRIMARY KEY,

    department VARCHAR(50) NOT NULL CHECK (
        department IN (
            'BRAIDING',
            'CARPET',
            'CUTTING',
            'DYEING',
            'EMBROIDERY',
            'KNITTING',
            'PRINTING',
            'QUILTING',
            'SEWING',
            'TUFTING',
            'WEAVING'
        )
    ),

    sr_no INT NOT NULL,
    machine_type VARCHAR(100) NOT NULL,
    component_spec TEXT NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,

    unit VARCHAR(20) NOT NULL CHECK (
        unit IN ('METER', 'KGS', 'PCS', 'LITRE')
    ),

    remarks TEXT,
    reference_image VARCHAR(255),   -- uploaded image path or URL

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Pantry
CREATE TABLE pantry_ui (
    id SERIAL PRIMARY KEY,
    entry_date DATE NOT NULL,

    sr_no INT NOT NULL,
    item VARCHAR(150) NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,

    unit VARCHAR(20) NOT NULL CHECK (
        unit IN ('METER', 'KGS', 'PCS', 'LITRE')
    ),

    item_for VARCHAR(20) NOT NULL CHECK (
        item_for IN ('COMPANY', 'GUEST')
    ),

    remarks TEXT,
    reference_image VARCHAR(255),   -- stores uploaded image path or URL

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--IT
CREATE TABLE it_ui (
    id SERIAL PRIMARY KEY,
    entry_date DATE NOT NULL,

    sr_no INT NOT NULL,
    item_description TEXT NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,

    unit VARCHAR(20) NOT NULL CHECK (
        unit IN ('METER', 'KGS', 'PCS', 'LITRE')
    ),

    remarks TEXT,
    reference_image VARCHAR(255),   -- stores uploaded image path or URL

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Housekeeping
CREATE TABLE house_keeping_ui (
    id SERIAL PRIMARY KEY,
    entry_date DATE NOT NULL,

    sr_no INT NOT NULL,
    item_description TEXT NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,

    unit VARCHAR(20) NOT NULL CHECK (
        unit IN ('METER', 'KGS', 'PCS', 'LITRE')
    ),

    remarks TEXT,
    reference_image VARCHAR(255),   -- stores uploaded image path or URL

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


--PO TABLE
CREATE TABLE purchase_orders (
    po_id                 BIGSERIAL PRIMARY KEY,
    po_code               VARCHAR(50) UNIQUE NOT NULL,
    order_date            DATE NOT NULL,
    order_time            TIME NOT NULL,
    factory_po_number     VARCHAR(100) NOT NULL,
    buyer_id              BIGINT NOT NULL,
    vendor_id             BIGINT NOT NULL,
    product_category      VARCHAR(100) NOT NULL,
    category_code         VARCHAR(50) NOT NULL,
    po_description        TEXT NOT NULL,
    particulars           TEXT NOT NULL,
    quantity              NUMERIC(12,0) NOT NULL,
    unit_rate             NUMERIC(12,2) NOT NULL,
    amount                NUMERIC(14,2) NOT NULL,
    delivery_date         DATE NOT NULL,
    payment_terms         TEXT NOT NULL,
    remarks               TEXT,
    last_po_number        VARCHAR(100),
    created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_po_buyer
        FOREIGN KEY (buyer_id) REFERENCES buyers(buyer_id),
    CONSTRAINT fk_po_vendor
        FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

--SECTION MASTER TABLES
CREATE TABLE part2_sections (
    section_id SMALLSERIAL PRIMARY KEY,
    section_code TEXT UNIQUE NOT NULL,
    section_name TEXT NOT NULL
);

CREATE TABLE part3_sections (
    section_id SMALLSERIAL PRIMARY KEY,
    section_code TEXT UNIQUE NOT NULL,
    section_name TEXT NOT NULL
); 
CREATE TABLE part4_sections (
    section_id SMALLSERIAL PRIMARY KEY,
    section_code TEXT UNIQUE NOT NULL,
    section_name TEXT NOT NULL
);

CREATE TABLE ta_sections (
    section_id SMALLSERIAL PRIMARY KEY,
    section_code TEXT UNIQUE NOT NULL,
    section_name TEXT NOT NULL
);

--PART 0 — PRODUCT SPECIFICATIONS
CREATE TABLE products (
    product_id BIGSERIAL PRIMARY KEY,
	buyer_sku TEXT NOT NULL,
    product_name TEXT NOT NULL,
	set_of SMALLINT NOT NULL,
    po_quantity INTEGER CHECK (po_quantity >= 1) NOT NULL,
    overage_percent NUMERIC CHECK (overage_percent BETWEEN 0 AND 100) NOT NULL,
	delivery_due_date DATE NOT NULL,
	image TEXT NOT NULL
   
);

CREATE TABLE subproducts(
	subproduct_id BIGSERIAL PRIMARY KEY,
	buyer_sku TEXT NOT NULL,
    subproduct_name TEXT NOT NULL,
    po_quantity INTEGER CHECK (po_quantity >= 1) NOT NULL,
    overage_percent NUMERIC CHECK (overage_percent BETWEEN 0 AND 100) NOT NULL,
	delivery_due_date DATE NOT NULL,
	image TEXT NOT NULL
);

--PART 1 — CUT & SEW
CREATE TABLE cut_sew_specs (
    cass_id BIGSERIAL PRIMARY KEY,
    component_name VARCHAR(27) NOT NULL,
    unit TEXT NOT NULL,
    gsm NUMERIC CHECK (gsm >= 0) NOT NULL,
	wastage NUMERIC NOT NULL,
    length_cut NUMERIC CHECK (length_cut >= 0) NOT NULL,
    width_cut NUMERIC CHECK (width_cut >= 0) NOT NULL,
    length_sew NUMERIC CHECK (length_sew >= 0) NOT NULL,
    width_sew NUMERIC CHECK (width_sew >= 0) NOT NULL
);


--MAIN MASTER TABLE 
CREATE TABLE main_master (
    main_id     BIGSERIAL PRIMARY KEY,

    -- Human-readable identifier for search
    reference_code TEXT NOT NULL UNIQUE,

    description TEXT,

    status      TEXT DEFAULT 'DRAFT',   -- DRAFT / ACTIVE / HOLD / CLOSED
    created_at  TIMESTAMP DEFAULT now(),
    updated_at  TIMESTAMP DEFAULT now()
);

--PART 2 - RAW MATERIAL AND SOURCING
--COMMON DETAILS
CREATE TABLE raw_materials (
    raw_material_id BIGSERIAL PRIMARY KEY,
    product_id BIGINT REFERENCES products(product_id) ON DELETE CASCADE,
    component_name VARCHAR(27) NOT NULL,
    material_description TEXT NOT NULL,
    net_consumption SMALLINT CHECK (net_consumption >= 1) NOT NULL,
    unit TEXT NOT NULL,
    work_order TEXT NOT NULL
);

--part 2 master table
CREATE TABLE part2_master (
    part2_id BIGSERIAL PRIMARY KEY,

    main_id BIGINT NOT NULL
        REFERENCES main_master(main_id)
        ON DELETE CASCADE,
		
    reference_code TEXT NOT NULL,   -- for search / UI identification
    remarks TEXT,

    status TEXT DEFAULT 'DRAFT',     -- DRAFT / ACTIVE / HOLD / CLOSED
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

--YARN
CREATE TABLE yarn_general (
    yarn_general_id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    fiber_type TEXT NOT NULL,
    yarn_name TEXT NOT NULL,
    composition TEXT NOT NULL,
    count_system TEXT,
    yarn_count TEXT,
    doubling TEXT,
    ply INTEGER,
    winding TEXT,

    surplus_percent NUMERIC,
    approval TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE yarn_advance (
    yarn_advance_id BIGSERIAL PRIMARY KEY,

    yarn_general_id BIGINT NOT NULL
        REFERENCES yarn_general(yarn_general_id)
        ON DELETE CASCADE,

    spinning_type TEXT,
    testing_requirements TEXT,
    fiber_category TEXT,
    origin TEXT,
    certifications TEXT,

    created_at TIMESTAMP DEFAULT now()
);

--FABRIC
CREATE TABLE fabric_general (
    fabric_general_id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    fiber_type TEXT NOT NULL,
    fabric_name TEXT NOT NULL,
    composition TEXT NOT NULL,
    gsm NUMERIC,
    surplus_percent NUMERIC,
    approval TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE fabric_advance (
    fabric_advance_id BIGSERIAL PRIMARY KEY,

    fabric_general_id BIGINT NOT NULL
        REFERENCES fabric_general(fabric_general_id)
        ON DELETE CASCADE,

    construction_type TEXT,
    weave_knit_type TEXT,
    machine_type TEXT,
    testing_requirements TEXT,
    fiber_category TEXT,
    origin TEXT,
    certifications TEXT,

    created_at TIMESTAMP DEFAULT now()
);

--FOAM
--eva foam
CREATE TABLE eva_foam_general (
    eva_foam_general_id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    foam_type TEXT,
    subtype TEXT,
    va_content TEXT,
    colour TEXT,
    thickness_mm NUMERIC,
    shape_ref_image TEXT,
    size_spec TEXT,
    gsm NUMERIC,
    length_cm NUMERIC,
    width_cm NUMERIC,
    qty_yardage_cns NUMERIC,
    kgs_cns NUMERIC,
    testing_requirements TEXT,
    surplus_percent NUMERIC,
    wastage_percent NUMERIC,
    approval TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE eva_foam_advance (
    eva_foam_advance_id BIGSERIAL PRIMARY KEY,

    eva_foam_general_id BIGINT NOT NULL
        REFERENCES eva_foam_general(eva_foam_general_id)
        ON DELETE CASCADE,

    shore_hardness TEXT,
    cell_structure TEXT,
    compression_set TEXT,
    tensile_strength TEXT,
    elongation TEXT,
    water_resistance TEXT,
    uv_resistance TEXT,
    fire_retardant TEXT,
    surface_texture TEXT,
    anti_slip TEXT,
    interlocking TEXT,
    certification TEXT,
    density TEXT,

    created_at TIMESTAMP DEFAULT now()
);

--gel-infused foam
CREATE TABLE gel_foam_general (
    gel_foam_general_id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    foam_type TEXT,
    base_foam TEXT,
    gel_type TEXT,
    gel_content TEXT,
    subtype TEXT,
    colour TEXT,
    thickness_mm NUMERIC,
    shape_ref_image TEXT,
    size_spec TEXT,
    gsm NUMERIC,
    length_cm NUMERIC,
    width_cm NUMERIC,
    qty_yardage_cns NUMERIC,
    kgs_cns NUMERIC,
    testing_requirements TEXT,
    surplus_percent NUMERIC,
    wastage_percent NUMERIC,
    approval TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE gel_foam_advance (
    gel_foam_advance_id BIGSERIAL PRIMARY KEY,

    gel_foam_general_id BIGINT NOT NULL
        REFERENCES gel_foam_general(gel_foam_general_id)
        ON DELETE CASCADE,

    density TEXT,
    ild_ifd TEXT,
    temperature_regulation TEXT,
    response_time TEXT,
    breathability TEXT,
    fire_retardant TEXT,
    cooling_effect TEXT,
    certification TEXT,

    created_at TIMESTAMP DEFAULT now()
);

--hr foam
CREATE TABLE hr_foam_general (
    hr_foam_general_id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    foam_type TEXT,
    subtype TEXT,
    grade TEXT,
    colour TEXT,
    thickness_mm NUMERIC,
    shape_ref_image TEXT,
    size_spec TEXT,
    gsm NUMERIC,
    length_cm NUMERIC,
    width_cm NUMERIC,
    qty_yardage_cns NUMERIC,
    kgs_cns NUMERIC,
    testing_requirements TEXT,
    surplus_percent NUMERIC,
    wastage_percent NUMERIC,
    approval TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE hr_foam_advance (
    hr_foam_advance_id BIGSERIAL PRIMARY KEY,

    hr_foam_general_id BIGINT NOT NULL
        REFERENCES hr_foam_general(hr_foam_general_id)
        ON DELETE CASCADE,

    ild_ifd TEXT,
    support_factor TEXT,
    resilience TEXT,
    compression_set TEXT,
    tensile_strength TEXT,
    elongation TEXT,
    fatigue_resistance TEXT,
    fire_retardant TEXT,
    certification TEXT,
    density TEXT,

    created_at TIMESTAMP DEFAULT now()
);

--latex foam
CREATE TABLE latex_foam_general (
    latex_foam_general_id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    foam_type TEXT,
    latex_type TEXT,
    natural_content TEXT,
    process TEXT,
    subtype TEXT,
    colour TEXT,
    thickness_mm NUMERIC,
    shape_ref_image TEXT,
    size_spec TEXT,
    gsm NUMERIC,
    length_cm NUMERIC,
    width_cm NUMERIC,
    qty_yardage_cns NUMERIC,
    kgs_cns NUMERIC,
    testing_requirements TEXT,
    surplus_percent NUMERIC,
    wastage_percent NUMERIC,
    approval TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE latex_foam_advance (
    latex_foam_advance_id BIGSERIAL PRIMARY KEY,

    latex_foam_general_id BIGINT NOT NULL
        REFERENCES latex_foam_general(latex_foam_general_id)
        ON DELETE CASCADE,

    ild_ifd TEXT,
    resilience TEXT,
    compression_set TEXT,
    pincore_pattern TEXT,
    zone_configuration TEXT,
    breathability TEXT,
    hypoallergenic TEXT,
    anti_microbial TEXT,
    fire_retardant TEXT,
    certification TEXT,
    density TEXT,

    created_at TIMESTAMP DEFAULT now()
);

--memory foam
CREATE TABLE memory_foam_general (
    memory_foam_general_id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    foam_type TEXT,
    subtype TEXT,
    grade TEXT,
    colour TEXT,
    thickness_mm NUMERIC,
    shape_ref_image TEXT,
    size_spec TEXT,
    gsm NUMERIC,
    length_cm NUMERIC,
    width_cm NUMERIC,
    qty_yardage_cns NUMERIC,
    kgs_cns NUMERIC,
    testing_requirements TEXT,
    surplus_percent NUMERIC,
    wastage_percent NUMERIC,
    approval TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE memory_foam_advance (
    memory_foam_advance_id BIGSERIAL PRIMARY KEY,

    memory_foam_general_id BIGINT NOT NULL
        REFERENCES memory_foam_general(memory_foam_general_id)
        ON DELETE CASCADE,

    ild_ifd TEXT,
    response_time TEXT,
    temperature_sensitivity TEXT,
    activation_temperature TEXT,
    compression_set TEXT,
    resilience TEXT,
    breathability TEXT,
    infusion TEXT,
    cooling_technology TEXT,
    fire_retardant TEXT,
    voc_emissions TEXT,
    certification TEXT,
    density TEXT,

    created_at TIMESTAMP DEFAULT now()
);

--pe/epe foam
CREATE TABLE pe_epe_foam_general (
    pe_epe_foam_general_id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    foam_type TEXT,
    subtype TEXT,
    colour TEXT,
    thickness_mm NUMERIC,
    shape_ref_image TEXT,
    size_spec TEXT,
    gsm NUMERIC,
    length_cm NUMERIC,
    width_cm NUMERIC,
    qty_yardage_cns NUMERIC,
    kgs_cns NUMERIC,
    testing_requirements TEXT,
    surplus_percent NUMERIC,
    wastage_percent NUMERIC,
    approval TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE pe_epe_foam_advance (
    pe_epe_foam_advance_id BIGSERIAL PRIMARY KEY,

    pe_epe_foam_general_id BIGINT NOT NULL
        REFERENCES pe_epe_foam_general(pe_epe_foam_general_id)
        ON DELETE CASCADE,

    cell_structure TEXT,
    lamination TEXT,
    cross_linked TEXT,
    anti_static TEXT,
    water_resistance TEXT,
    cushioning TEXT,
    fire_retardant TEXT,
    thermal_insulation TEXT,
    certification TEXT,
    density TEXT,

    created_at TIMESTAMP DEFAULT now()
);

--pu foam
CREATE TABLE pu_foam_general (
    pu_foam_general_id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    foam_type TEXT,
    subtype TEXT,
    grade TEXT,
    colour TEXT,
    thickness_mm NUMERIC,
    shape_ref_image TEXT,
    size_spec TEXT,
    gsm NUMERIC,
    length_cm NUMERIC,
    width_cm NUMERIC,
    qty_yardage_cns NUMERIC,
    kgs_cns NUMERIC,
    testing_requirements TEXT,
    surplus_percent NUMERIC,
    wastage_percent NUMERIC,
    approval TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE pu_foam_advance (
    pu_foam_advance_id BIGSERIAL PRIMARY KEY,

    pu_foam_general_id BIGINT NOT NULL
        REFERENCES pu_foam_general(pu_foam_general_id)
        ON DELETE CASCADE,

    ild_ifd TEXT,
    support_factor TEXT,
    resilience TEXT,
    cell_structure TEXT,
    compression_set TEXT,
    tensile_strength TEXT,
    elongation TEXT,
    anti_microbial TEXT,
    fire_retardant TEXT,
    certification TEXT,
    density TEXT,

    created_at TIMESTAMP DEFAULT now()
);

--rebonded foam
CREATE TABLE rebonded_foam_general (
    rebonded_foam_general_id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    foam_type TEXT,
    subtype TEXT,
    chip_source TEXT,
    chip_size TEXT,
    bonding TEXT,
    colour TEXT,
    thickness_mm NUMERIC,
    shape_ref_image TEXT,
    size_spec TEXT,
    gsm NUMERIC,
    length_cm NUMERIC,
    width_cm NUMERIC,
    qty_yardage_cns NUMERIC,
    kgs_cns NUMERIC,
    testing_requirements TEXT,
    surplus_percent NUMERIC,
    wastage_percent NUMERIC,
    approval TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE rebonded_foam_advance (
    rebonded_foam_advance_id BIGSERIAL PRIMARY KEY,

    rebonded_foam_general_id BIGINT NOT NULL
        REFERENCES rebonded_foam_general(rebonded_foam_general_id)
        ON DELETE CASCADE,

    ild_ifd TEXT,
    compression_set TEXT,
    fire_retardant TEXT,
    certification TEXT,
    density TEXT,

    created_at TIMESTAMP DEFAULT now()
);

--FIBER
--Cotton fill
CREATE TABLE cotton_fill_general (
    cotton_fill_general_id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    fiber_type TEXT,
    subtype TEXT,
    form TEXT,
    grade TEXT,
    colour TEXT,

    qty_kgs NUMERIC,
    size_spec TEXT,
    gsm NUMERIC,
    length_cm NUMERIC,
    width_cm NUMERIC,
    qty_yardage NUMERIC,
    qty_kgs_cns NUMERIC,

    testing TEXT,
    testing_upload TEXT,

    surplus_percent NUMERIC,
    wastage_percent NUMERIC,
    approval TEXT,
    remarks TEXT
);

CREATE TABLE cotton_fill_advance (
    cotton_fill_advance_id BIGSERIAL PRIMARY KEY,

    cotton_fill_general_id BIGINT NOT NULL
        REFERENCES cotton_fill_general(cotton_fill_general_id)
        ON DELETE CASCADE,

    staple_length TEXT,
    processing TEXT,
    bonding TEXT,
    needle_punched TEXT,
    fire_retardant TEXT,
    dust_trash_content TEXT,
    organic_certified TEXT
);

--Down Alternative
CREATE TABLE down_alternative_general (
    down_alt_general_id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    fiber_type TEXT,
    subtype TEXT,
    form TEXT,
    construction TEXT,
    denier TEXT,
    siliconized TEXT,

    qty_kgs NUMERIC,
    size_spec TEXT,
    gsm NUMERIC,
    length_cm NUMERIC,
    width_cm NUMERIC,
    qty_yardage NUMERIC,
    qty_kgs_cns NUMERIC,

    testing_requirements TEXT,
    testing_upload TEXT,

    surplus_percent NUMERIC,
    wastage_percent NUMERIC,
    approval TEXT,
    remarks TEXT
);

CREATE TABLE down_alternative_advance (
    down_alt_advance_id BIGSERIAL PRIMARY KEY,

    down_alt_general_id BIGINT NOT NULL
        REFERENCES down_alternative_general(down_alt_general_id)
        ON DELETE CASCADE,

    loft_rating TEXT,
    fill_power_equivalent TEXT,
    warmth_to_weight TEXT,
    water_resistance TEXT,
    quick_dry TEXT,
    hypoallergenic TEXT,
    anti_microbial TEXT,
    vegan_cruelty_free TEXT,
    machine_washable TEXT,
    certification TEXT
);

--Down and Feather
CREATE TABLE down_feather_general (
    down_feather_general_id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    fiber_type TEXT,
    bird_type TEXT,
    origin TEXT,
    down_percentage TEXT,
    colour TEXT,
    down_proof_required TEXT,
    traceability TEXT,

    qty_kgs NUMERIC,
    size_spec TEXT,
    gsm NUMERIC,
    length_cm NUMERIC,
    width_cm NUMERIC,
    qty_yardage NUMERIC,
    qty_kgs_cns NUMERIC,

    testing_requirements TEXT,
    testing_upload TEXT,

    surplus_percent NUMERIC,
    wastage_percent NUMERIC,
    approval TEXT,
    remarks TEXT
);

CREATE TABLE down_feather_advance (
    down_feather_advance_id BIGSERIAL PRIMARY KEY,

    down_feather_general_id BIGINT NOT NULL
        REFERENCES down_feather_general(down_feather_general_id)
        ON DELETE CASCADE,

    fill_power TEXT,
    processing TEXT,
    oxygen_number TEXT,
    turbidity TEXT,
    odor TEXT,
    anti_microbial TEXT,
    cluster_size TEXT,
    certification TEXT
);

--microfiber
CREATE TABLE microfiber_fill_general (
    microfiber_general_id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    fiber_type TEXT,
    subtype TEXT,
    form TEXT,
    denier TEXT,
    siliconized TEXT,
    colour TEXT,

    qty_kgs NUMERIC,
    size_spec TEXT,
    gsm NUMERIC,
    length_cm NUMERIC,
    width_cm NUMERIC,
    qty_yardage NUMERIC,
    qty_kgs_cns NUMERIC,

    testing_requirements TEXT,
    testing_upload TEXT,

    surplus_percent NUMERIC,
    wastage_percent NUMERIC,
    approval TEXT,
    remarks TEXT
);

CREATE TABLE microfiber_fill_advance (
    microfiber_advance_id BIGSERIAL PRIMARY KEY,

    microfiber_general_id BIGINT NOT NULL
        REFERENCES microfiber_fill_general(microfiber_general_id)
        ON DELETE CASCADE,

    fiber_length TEXT,
    structure TEXT,
    cluster_type TEXT,
    cluster_size TEXT,
    loft_fill_power TEXT,
    hand_feel TEXT,
    anti_microbial TEXT,
    hypoallergenic TEXT,
    certification TEXT
);

--polyester
CREATE TABLE polyester_fill_general (
    polyester_general_id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    fiber_type TEXT,
    subtype TEXT,
    denier TEXT,
    siliconized TEXT,
    conjugate_crimp TEXT,
    colour TEXT,

    qty_kgs NUMERIC,
    size_spec TEXT,
    gsm NUMERIC,
    length_cm NUMERIC,
    width_cm NUMERIC,
    qty_yardage NUMERIC,
    qty_kgs_cns NUMERIC,

    testing TEXT,
    testing_upload TEXT,

    surplus_percent NUMERIC,
    wastage_percent NUMERIC,
    approval TEXT,
    remarks TEXT
);

CREATE TABLE polyester_fill_advance (
    polyester_advance_id BIGSERIAL PRIMARY KEY,

    polyester_general_id BIGINT NOT NULL
        REFERENCES polyester_fill_general(polyester_general_id)
        ON DELETE CASCADE,

    fiber_length TEXT,
    structure TEXT,
    thermal_bonded TEXT,
    anti_microbial TEXT,
    fire_retardant TEXT,
    certification TEXT,
    loft TEXT
);

--specialty
CREATE TABLE specialty_fill_general (
    specialty_general_id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    fiber_type TEXT,
    eco_certification TEXT,
    form TEXT,

    qty_kgs NUMERIC,
    size_spec TEXT,
    gsm NUMERIC,
    length_cm NUMERIC,
    width_cm NUMERIC,
    qty_yardage NUMERIC,
    qty_kgs_cns NUMERIC,

    testing_requirements TEXT,
    testing_upload TEXT,

    surplus_percent NUMERIC,
    wastage_percent NUMERIC,
    approval TEXT,
    remarks TEXT
);

CREATE TABLE specialty_fill_advance (
    specialty_advance_id BIGSERIAL PRIMARY KEY,

    specialty_general_id BIGINT NOT NULL
        REFERENCES specialty_fill_general(specialty_general_id)
        ON DELETE CASCADE,

    blending TEXT,
    biodegradable TEXT,

    kapok_source TEXT,
    kapok_properties TEXT,

    bamboo_type TEXT,
    bamboo_properties TEXT,

    silk_floss_type TEXT,
    silk_floss_grade TEXT,

    recycled_source TEXT,
    recycled_certification TEXT,

    tencel_type TEXT
);

--wool
CREATE TABLE wool_natural_general (
    wool_general_id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    fiber_type TEXT,
    wool_type TEXT,
    subtype TEXT,
    form TEXT,
    micron TEXT,
    colour TEXT,

    qty_kgs NUMERIC,
    size_spec TEXT,
    gsm NUMERIC,
    length_cm NUMERIC,
    width_cm NUMERIC,
    qty_yardage NUMERIC,
    qty_kgs_cns NUMERIC,

    testing_requirements TEXT,
    testing_upload TEXT,

    surplus_percent NUMERIC,
    wastage_percent NUMERIC,
    approval TEXT,
    remarks TEXT
);

CREATE TABLE wool_natural_advance (
    wool_advance_id BIGSERIAL PRIMARY KEY,

    wool_general_id BIGINT NOT NULL
        REFERENCES wool_natural_general(wool_general_id)
        ON DELETE CASCADE,

    processing TEXT,
    lanolin_content TEXT,
    temperature_regulating TEXT,
    moisture_wicking TEXT,
    fire_retardant TEXT,
    mulesing_free TEXT,
    organic_certified TEXT
);

--TRIMS AND ACCESSORIES
--Cable ties
CREATE TABLE ta_cable_ties (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    tie_type TEXT NOT NULL,              -- Nylon / Metal / Releasable etc.
    material TEXT NOT NULL,

    size_cm NUMERIC
        CHECK (size_cm > 0),             -- Length in CM

    colour TEXT,
    placement TEXT,                      -- text + image ref handled at UI level

    testing_requirement TEXT,

    quantity INTEGER NOT NULL
        CHECK (quantity > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE ta_cable_tie_specs (
    id BIGSERIAL PRIMARY KEY,

    cable_tie_id BIGINT NOT NULL
        REFERENCES ta_cable_ties(id)
        ON DELETE CASCADE,

    tensile_strength TEXT,       -- e.g. 18kg / 50kg / Heavy duty
    finish TEXT,                 -- Natural / Black / Polished
    uv_resistance TEXT,          -- Yes / No / UV stabilized

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    CONSTRAINT uq_cable_tie_specs UNIQUE (cable_tie_id)
); 

--Cord stops
CREATE TABLE ta_cord_stops (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    stop_type TEXT NOT NULL,               -- Single hole / Double hole / Toggle
    material TEXT NOT NULL,

    size_cm NUMERIC
        CHECK (size_cm > 0),

    colour TEXT,
    locking_mechanism TEXT,                -- Spring / Push / Manual

    placement TEXT,                        -- text + image ref handled in UI
    testing_requirement TEXT,

    quantity INTEGER NOT NULL
        CHECK (quantity > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE ta_cord_stop_specs (
    id BIGSERIAL PRIMARY KEY,

    cord_stop_id BIGINT NOT NULL
        REFERENCES ta_cord_stops(id)
        ON DELETE CASCADE,

    function TEXT,          -- Adjuster / Lock / Decorative
    breakaway TEXT,         -- Yes / No / Child-safety compliant

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    CONSTRAINT uq_cord_stop_specs UNIQUE (cord_stop_id)
);

--felts
CREATE TABLE ta_felts (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    felt_type TEXT NOT NULL,                 -- Needle felt / Pressed / Wool blend
    material TEXT NOT NULL,

    colour TEXT,                             -- colour name
    colour_reference TEXT,                   -- image/file ref handled at app layer

    gsm NUMERIC
        CHECK (gsm > 0),

    length_cm NUMERIC
        CHECK (length_cm > 0),

    width_cm NUMERIC
        CHECK (width_cm > 0),

    quantity_value NUMERIC NOT NULL
        CHECK (quantity_value > 0),

    quantity_unit TEXT NOT NULL,             -- YARDAGE / KGS
    testing_requirement TEXT,

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE ta_felt_specs (
    id BIGSERIAL PRIMARY KEY,

    felt_id BIGINT NOT NULL
        REFERENCES ta_felts(id)
        ON DELETE CASCADE,

    thickness TEXT,          -- mm / micron / grade
    finish_form TEXT,        -- smooth / rough / embossed
    application TEXT,        -- padding / insulation / packaging
    stiffness TEXT,          -- soft / medium / rigid

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    CONSTRAINT uq_felt_specs UNIQUE (felt_id)
);

--hooks eyes
CREATE TABLE ta_hooks_eyes (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    hook_eye_type TEXT NOT NULL,              -- hook & eye / eye only / hook only
    material TEXT NOT NULL,

    size TEXT NOT NULL,                       -- size code / mm reference
    colour TEXT,
    finish_type TEXT,

    placement TEXT,                           -- sewing placement notes
    placement_reference TEXT,                 -- image ref handled in app

    quantity_value NUMERIC NOT NULL
        CHECK (quantity_value > 0),

    quantity_unit TEXT NOT NULL,              -- PAIR_PER_PC

    testing_requirement TEXT,

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE ta_hook_eye_specs (
    id BIGSERIAL PRIMARY KEY,

    hook_eye_id BIGINT NOT NULL
        REFERENCES ta_hooks_eyes(id)
        ON DELETE CASCADE,

    strength TEXT,            -- light / medium / heavy / kg rating
    application TEXT,         -- lingerie / outerwear / sports / kids

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    CONSTRAINT uq_hook_eye_specs UNIQUE (hook_eye_id)
);

--interlining
CREATE TABLE ta_interlinings (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    interlining_type TEXT NOT NULL,          -- woven / non-woven / knit
    material TEXT NOT NULL,

    adhesive_type TEXT NOT NULL,             -- PA / PES / HDPE etc.
    colour TEXT,

    placement TEXT,                          -- collar / placket / waistband
    placement_reference TEXT,                -- image reference (UI upload)

    gsm NUMERIC CHECK (gsm > 0),
    length_cm NUMERIC CHECK (length_cm > 0),
    width_cm NUMERIC CHECK (width_cm > 0),

    quantity_value NUMERIC NOT NULL
        CHECK (quantity_value > 0),

    quantity_unit TEXT NOT NULL,              -- YARDAGE / KGS
    cons_per_pc BOOLEAN DEFAULT FALSE,        -- CNS per PC checkbox

    testing_requirement TEXT,

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE ta_interlining_specs (
    id BIGSERIAL PRIMARY KEY,

    interlining_id BIGINT NOT NULL
        REFERENCES ta_interlinings(id)
        ON DELETE CASCADE,

    dot_density TEXT,        -- dots/cm², fine/medium/heavy
    stretch TEXT,            -- none / weft / warp / both
    fusing_spec TEXT,        -- temp, pressure, dwell time
    hand_feel TEXT,          -- soft / crisp / firm

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    CONSTRAINT uq_interlining_specs UNIQUE (interlining_id)
);

--magnetic closure
CREATE TABLE ta_magnetic_closures (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    closure_type TEXT NOT NULL,        -- button / snap / hidden / sew-in
    material TEXT NOT NULL,

    size_cm NUMERIC CHECK (size_cm > 0),
    strength TEXT NOT NULL,            -- light / medium / heavy / kg rating

    placement TEXT,
    placement_reference TEXT,          -- image upload reference

    testing_requirement TEXT,

    quantity_pairs INTEGER NOT NULL
        CHECK (quantity_pairs > 0),    -- male/female set per PC

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE ta_magnetic_closure_specs (
    id BIGSERIAL PRIMARY KEY,

    magnetic_closure_id BIGINT NOT NULL
        REFERENCES ta_magnetic_closures(id)
        ON DELETE CASCADE,

    polarity TEXT,          -- north-south / auto-align
    application TEXT,       -- sewn-in / embedded / heat-sealed
    encasing TEXT,          -- plastic / metal / fabric wrapped
    shielding TEXT,         -- EMI shield / card-safe / none
	

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    CONSTRAINT uq_magnetic_closure_specs
        UNIQUE (magnetic_closure_id)
);

--barbs
CREATE TABLE ta_pins_barbs (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    pin_type TEXT NOT NULL,          -- pin / barb / loop / plastic fastener
    material TEXT NOT NULL,

    size_cm NUMERIC CHECK (size_cm > 0),
    colour TEXT NOT NULL,
    head_type TEXT NOT NULL,          -- T-head / paddle / round / etc.

    placement TEXT,
    placement_reference TEXT,         -- upload reference image

    testing_requirement TEXT,

    quantity_pairs INTEGER NOT NULL
        CHECK (quantity_pairs > 0),   -- pair per PC

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE ta_pins_barbs_specs (
    id BIGSERIAL PRIMARY KEY,

    pins_barbs_id BIGINT NOT NULL
        REFERENCES ta_pins_barbs(id)
        ON DELETE CASCADE,

    tensile_strength TEXT,        -- kg / N / vendor rating
    application TEXT,             -- hand / tagging gun / auto
    magazine_cartridge TEXT,      -- compatible gun / cartridge type

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    CONSTRAINT uq_pins_barbs_specs
        UNIQUE (pins_barbs_id)
);

--reflective tape
CREATE TABLE ta_reflective_tapes (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    tape_type TEXT NOT NULL,
    material TEXT NOT NULL,
    colour TEXT NOT NULL,
    base_fabric TEXT,

    placement TEXT,
    placement_reference TEXT,          -- upload reference image

    testing_requirement TEXT,          -- dropdown/multiselect (stored text)
    testing_document TEXT,             -- upload

    gsm NUMERIC CHECK (gsm > 0),
    length_cm NUMERIC CHECK (length_cm > 0),
    width_cm NUMERIC CHECK (width_cm > 0),

    quantity_yardage NUMERIC CHECK (quantity_yardage >= 0),
    quantity_kgs NUMERIC CHECK (quantity_kgs >= 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE ta_reflective_tapes_specs (
    id BIGSERIAL PRIMARY KEY,

    reflective_tape_id BIGINT NOT NULL
        REFERENCES ta_reflective_tapes(id)
        ON DELETE CASCADE,

    certification TEXT,        -- EN ISO, ANSI, etc.
    wash_durability TEXT,      -- number of washes / standard
    reflectivity TEXT,         -- cd/lx/m² or grade

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    CONSTRAINT uq_reflective_tapes_specs
        UNIQUE (reflective_tape_id)
);

--rings loops
CREATE TABLE ta_rings_loops (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    ring_loop_type TEXT NOT NULL,
    material TEXT NOT NULL,

    size_cm NUMERIC CHECK (size_cm > 0),
    thickness_gauge TEXT,
    finish_plating TEXT,

    placement TEXT,
    placement_reference TEXT,          -- upload reference image

    testing_requirement TEXT,          -- dropdown / multiselect
    testing_document TEXT,             -- upload

    quantity_pcs INTEGER CHECK (quantity_pcs > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE ta_rings_loops_specs (
    id BIGSERIAL PRIMARY KEY,

    rings_loops_id BIGINT NOT NULL
        REFERENCES ta_rings_loops(id)
        ON DELETE CASCADE,

    load_rating TEXT,     -- kg / N / grade
    welded TEXT,          -- Yes / No / Type
    application TEXT,     -- functional usage

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    CONSTRAINT uq_rings_loops_specs
        UNIQUE (rings_loops_id)
);

--rivets
CREATE TABLE ta_rivets (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    rivet_type TEXT NOT NULL,
    material TEXT NOT NULL,

    cap_size TEXT,          -- dropdown / vendor-defined
    post_height TEXT,       -- dropdown / vendor-defined
    finish_plating TEXT,

    placement TEXT,
    placement_reference TEXT,   -- upload reference image

    testing_requirement TEXT,   -- dropdown / multiselect
    testing_document TEXT,      -- upload

    quantity_pcs INTEGER CHECK (quantity_pcs > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE ta_rivets_specs (
    id BIGSERIAL PRIMARY KEY,

    rivets_id BIGINT NOT NULL
        REFERENCES ta_rivets(id)
        ON DELETE CASCADE,

    logo TEXT,        -- logo / branding requirement
    setting TEXT,     -- hand press / machine / type

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    CONSTRAINT uq_rivets_specs
        UNIQUE (rivets_id)
);

--seam tape
CREATE TABLE ta_seam_tapes (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    tape_type TEXT NOT NULL,
    material TEXT NOT NULL,

    width_cm NUMERIC CHECK (width_cm > 0),

    colour TEXT,
    adhesive_type TEXT,

    placement TEXT,
    placement_reference TEXT,     -- upload reference image

    testing_requirement TEXT,     -- dropdown / multiselect
    testing_document TEXT,        -- upload

    quantity_meters NUMERIC CHECK (quantity_meters > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE ta_seam_tape_specs (
    id BIGSERIAL PRIMARY KEY,

    seam_tape_id BIGINT NOT NULL
        REFERENCES ta_seam_tapes(id)
        ON DELETE CASCADE,

    application_spec TEXT,
    elasticity TEXT,
    breathability TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    CONSTRAINT uq_seam_tape_specs
        UNIQUE (seam_tape_id)
);

--velcro
CREATE TABLE ta_velcro (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    part TEXT NOT NULL,              -- hook / loop / both
    velcro_type TEXT NOT NULL,
    material TEXT NOT NULL,
    attachment TEXT NOT NULL,        -- sew-on / adhesive / heat seal

    placement TEXT,
    placement_reference TEXT,        -- upload reference image

    testing_requirement TEXT,        -- dropdown / multiselect
    testing_document TEXT,           -- upload

    length_cm NUMERIC CHECK (length_cm > 0),
    width_cm NUMERIC CHECK (width_cm > 0),

    quantity_yardage NUMERIC CHECK (quantity_yardage >= 0),
    quantity_kgs NUMERIC CHECK (quantity_kgs >= 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE ta_velcro_specs (
    id BIGSERIAL PRIMARY KEY,

    velcro_id BIGINT NOT NULL
        REFERENCES ta_velcro(id)
        ON DELETE CASCADE,

    colour TEXT,
    colour_reference TEXT,        -- upload color reference

    hook_density TEXT,
    loop_type TEXT,
    cycle_life TEXT,
    flame_retardant TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    CONSTRAINT uq_velcro_specs
        UNIQUE (velcro_id)
);

--buckles
CREATE TABLE ta_buckles (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    buckle_type TEXT NOT NULL,          -- side release, ladder lock, cam, etc.
    material TEXT NOT NULL,

    webbing_width_cm NUMERIC
        CHECK (webbing_width_cm > 0),   -- SIZE = webbing width

    finish_colour TEXT NOT NULL,

    placement TEXT,
    placement_reference TEXT,           -- upload reference image

    testing_requirement TEXT,           -- dropdown / multiselect
    testing_document TEXT,              -- upload

    quantity_pcs INTEGER NOT NULL
        CHECK (quantity_pcs > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE ta_buckle_specs (
    id BIGSERIAL PRIMARY KEY,

    buckle_id BIGINT NOT NULL
        REFERENCES ta_buckles(id)
        ON DELETE CASCADE,

    function TEXT,              -- load bearing, decorative, adjustable
    tensile_strength TEXT,      -- dropdown values
    safety TEXT,                -- child-safe, breakaway, lock type

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    CONSTRAINT uq_buckle_specs
        UNIQUE (buckle_id)
);

--buttons
CREATE TABLE ta_buttons (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    button_type TEXT NOT NULL,        -- snap, shirt, shank, metal, etc.
    material TEXT NOT NULL,

    size_text TEXT NOT NULL,          -- original UI value (e.g. "24L", "18mm")
    size_ligne NUMERIC,               -- optional normalized value (1L = 0.635mm)

    holes TEXT,                       -- 2-hole, 4-hole, no-hole, etc.
    finish_colour TEXT NOT NULL,
    colour_reference TEXT,            -- upload color reference

    placement TEXT,
    placement_reference TEXT,         -- upload image reference

    testing_requirement TEXT,         -- dropdown / multiselect
    testing_document TEXT,            -- upload

    quantity_pcs INTEGER NOT NULL
        CHECK (quantity_pcs > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE ta_button_specs (
    id BIGSERIAL PRIMARY KEY,

    button_id BIGINT NOT NULL
        REFERENCES ta_buttons(id)
        ON DELETE CASCADE,

    attachment TEXT,      -- sew-on, snap-fit, riveted
    function TEXT,        -- decorative, functional, load-bearing
    logo TEXT,            -- debossed, engraved, printed, none

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    CONSTRAINT uq_button_specs
        UNIQUE (button_id)
);

--shoulder pads
CREATE TABLE ta_shoulder_pads (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    pad_type TEXT NOT NULL,           -- dropdown
    material TEXT NOT NULL,           -- dropdown

    size_spec TEXT NOT NULL,           -- LxW x Thickness OR Cup Size (A/B/C/D)
    thickness_cm NUMERIC
        CHECK (thickness_cm > 0),

    shape TEXT NOT NULL,              -- dropdown
    covering TEXT NOT NULL,           -- dropdown
    covering_colour TEXT NOT NULL,    -- dropdown
    attachment TEXT NOT NULL,          -- dropdown
    density TEXT NOT NULL,             -- dropdown

    placement TEXT,
    placement_reference TEXT,          -- upload reference image

    testing_requirement TEXT,          -- dropdown multiselect
    testing_document TEXT,             -- upload

    quantity_pairs INTEGER NOT NULL
        CHECK (quantity_pairs > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

--lace
CREATE TABLE ta_lace_general (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    lace_type TEXT NOT NULL,           -- dropdown
    material TEXT NOT NULL,            -- dropdown

    width_cm NUMERIC
        CHECK (width_cm > 0),

    colour TEXT NOT NULL,
    colour_reference TEXT,             -- upload color reference

    design_reference TEXT,             -- dropdown/text
    design_image TEXT,                 -- upload image reference

    placement TEXT,
    placement_image TEXT,              -- upload placement reference

    testing_requirement TEXT,          -- dropdown multiselect
    testing_document TEXT,             -- upload

    gsm NUMERIC
        CHECK (gsm > 0),

    length_cm NUMERIC
        CHECK (length_cm > 0),

    width_spec_cm NUMERIC
        CHECK (width_spec_cm > 0),

    quantity_yardage NUMERIC
        CHECK (quantity_yardage >= 0),

    quantity_kgs NUMERIC
        CHECK (quantity_kgs >= 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE ta_lace_advance (
    id BIGSERIAL PRIMARY KEY,

    lace_general_id BIGINT NOT NULL
        REFERENCES ta_lace_general(id)
        ON DELETE CASCADE,

    finishing TEXT,        -- dropdown
    stretch TEXT,          -- dropdown
    pattern_type TEXT,     -- dropdown

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

--ribbing
CREATE TABLE ta_ribbing_general (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    ribbing_type TEXT NOT NULL,          -- dropdown
    material TEXT NOT NULL,              -- dropdown

    colour TEXT NOT NULL,                -- DTM / Pantone TCX
    colour_reference TEXT,               -- upload reference image

    placement TEXT,
    placement_image TEXT,                -- upload

    testing_requirements TEXT,           -- dropdown multiselect
    testing_document TEXT,               -- upload

    gsm NUMERIC
        CHECK (gsm > 0),

    form TEXT CHECK (form IN ('TUBULAR', 'ROLL')),

    -- Tubular-specific
    tubular_length_cm NUMERIC
        CHECK (tubular_length_cm > 0),
    tubular_dia_cm NUMERIC
        CHECK (tubular_dia_cm > 0),

    -- Roll-specific
    roll_length_cm NUMERIC
        CHECK (roll_length_cm > 0),
    roll_width_cm NUMERIC
        CHECK (roll_width_cm > 0),

    quantity_yardage NUMERIC
        CHECK (quantity_yardage >= 0),

    quantity_kgs NUMERIC
        CHECK (quantity_kgs >= 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    -- Safety check to ensure correct dimension usage
    CHECK (
        (form = 'TUBULAR' AND tubular_length_cm IS NOT NULL AND tubular_dia_cm IS NOT NULL)
        OR
        (form = 'ROLL' AND roll_length_cm IS NOT NULL AND roll_width_cm IS NOT NULL)
    )
);

CREATE TABLE ta_ribbing_advance (
    id BIGSERIAL PRIMARY KEY,

    ribbing_general_id BIGINT NOT NULL
        REFERENCES ta_ribbing_general(id)
        ON DELETE CASCADE,

    stretch_percent TEXT,        -- dropdown
    cutting TEXT,                -- dropdown
    spandex_content TEXT,        -- dropdown
    anti_curl TEXT,              -- dropdown

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

--niwar
CREATE TABLE ta_niwar_webbing_general (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    

    webbing_type TEXT NOT NULL,        -- dropdown
    material TEXT NOT NULL,            -- dropdown

    colour TEXT NOT NULL,              -- DTM / White / Black / Natural / Pantone
    colour_reference TEXT,             -- upload colour reference

    weave_pattern TEXT,                -- dropdown

    placement TEXT,
    placement_image TEXT,              -- upload reference image

    testing_requirements TEXT,         -- dropdown multiselect
    testing_document TEXT,             -- upload

    gsm NUMERIC
        CHECK (gsm > 0),

    length_cm NUMERIC
        CHECK (length_cm > 0),

    width_cm NUMERIC
        CHECK (width_cm > 0),

    quantity_yardage NUMERIC
        CHECK (quantity_yardage >= 0),

    quantity_kgs NUMERIC
        CHECK (quantity_kgs >= 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE ta_niwar_webbing_advance (
    id BIGSERIAL PRIMARY KEY,

    webbing_general_id BIGINT NOT NULL
        REFERENCES ta_niwar_webbing_general(id)
        ON DELETE CASCADE,

    thickness TEXT,            -- dropdown
    finish TEXT,               -- dropdown
    tensile_strength TEXT,     -- dropdown
    edge_type TEXT,            -- dropdown

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- Paper Tubes (General)
CREATE TABLE ta_paper_tubes (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    tube_type TEXT NOT NULL,              -- Dropdown / Others
    material TEXT NOT NULL,               -- Dropdown / Others

    diameter_cm NUMERIC
        CHECK (diameter_cm > 0),

    length_cm NUMERIC
        CHECK (length_cm > 0),

    usage TEXT,                           -- free text / dropdown

    testing_requirements TEXT,            -- dropdown + multiselect (stored as text)

    quantity INTEGER NOT NULL
        CHECK (quantity > 0),             -- Pieces

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,                -- dropdown / others
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- Paper Tubes (Advanced Specs)
CREATE TABLE ta_paper_tube_specs (
    id BIGSERIAL PRIMARY KEY,

    paper_tube_id BIGINT NOT NULL
        REFERENCES ta_paper_tubes(id)
        ON DELETE CASCADE,

    colour TEXT,               -- Dropdown / Others
    end_caps TEXT,             -- Yes / No / Type
    flexibility TEXT,          -- Rigid / Semi / Flexible
    application TEXT,          -- Packaging / Support / Display etc.

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    CONSTRAINT uq_paper_tube_specs
        UNIQUE (paper_tube_id)
);

-- Zippers (General)
CREATE TABLE ta_zippers (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT
        REFERENCES part2_master(part2_id)
        ON DELETE CASCADE,

    zip_size TEXT,                     -- ZIP # (size)
    zipper_type TEXT,                  -- coil / metal / molded etc.
    brand TEXT,
    puller_type TEXT,

    length_value NUMERIC
        CHECK (length_value > 0),      -- inches unit at UI level

    colour TEXT,                       -- DTM / Standard / Pantone
    colour_reference TEXT,             -- uploaded colour ref

    placement TEXT,
    placement_reference TEXT,          -- uploaded image

    testing_requirements TEXT,         -- dropdown / multiselect
    size_spec_reference TEXT,          -- uploaded spec (length/width)

    size_length_cm NUMERIC
        CHECK (size_length_cm > 0),

    size_width_cm NUMERIC
        CHECK (size_width_cm > 0),

    quantity INTEGER
        CHECK (quantity > 0),          -- PCS

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- Zippers (Advanced Specs)
CREATE TABLE ta_zipper_specs (
    id BIGSERIAL PRIMARY KEY,

    zipper_id BIGINT
        REFERENCES ta_zippers(id)
        ON DELETE CASCADE,

    teeth_material TEXT,        -- dropdown / others
    puller_material TEXT,       -- dropdown / others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    CONSTRAINT uq_zipper_specs
        UNIQUE (zipper_id)
);

--Work Orders
--Weaving
CREATE TABLE part2_weaving_general (
    id BIGSERIAL PRIMARY KEY,

	part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    machine_type TEXT NOT NULL,          -- e.g. Water Jet
    design_ref TEXT NOT NULL,

    reed NUMERIC CHECK (reed > 0),
    pick NUMERIC CHECK (pick > 0),

    gsm NUMERIC CHECK (gsm > 0) NOT NULL,

    wastage NUMERIC
        CHECK (wastage BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part2_weaving_advanced (
    id BIGSERIAL PRIMARY KEY,

    weaving_general_id BIGINT NOT NULL
        REFERENCES part2_weaving_general(id)
        ON DELETE CASCADE,
		
    weaving_type TEXT NOT NULL,                  -- e.g. Water Jet
    variants TEXT,                       -- Standard / High-Speed Waterjet
    design TEXT NOT NULL,                -- Plain, Twill, Satin, etc.
    warp_ratio NUMERIC(4,3)
        CHECK (warp_ratio BETWEEN 0 AND 1)
        NOT NULL,

    weft_ratio NUMERIC(4,3)
        CHECK (weft_ratio BETWEEN 0 AND 1)
        NOT NULL,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (weaving_general_id)
);

--Tufting

CREATE TABLE part2_tufting_general (
    id BIGSERIAL PRIMARY KEY,

	part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    machine_type TEXT NOT NULL,         -- Table Top / CNC / Computerised
    design_ref TEXT NOT NULL,           -- Upload

    gsm NUMERIC CHECK (gsm > 0) NOT NULL,

    pile_height_mm NUMERIC
        CHECK (pile_height_mm > 0)
        NOT NULL,

    tpi SMALLINT
        CHECK (tpi > 0)
        NOT NULL,

    wastage NUMERIC
        CHECK (wastage BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,     -- Buyers / Initial / PP / Sample
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part2_tufting_advanced (
    id BIGSERIAL PRIMARY KEY,

    tufting_general_id BIGINT NOT NULL
        REFERENCES part2_tufting_general(id)
        ON DELETE CASCADE,

    design TEXT NOT NULL,               -- High-Low Loop, Cut Pile, etc.
    variants TEXT,                      -- CNC variants
    machine_gauge TEXT,                 -- 1/8, 1/10, 5/32, 5/64
    stitch_rate NUMERIC CHECK (stitch_rate > 0),

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (tufting_general_id)
);

--Quilting
CREATE TABLE part2_quilting_general (
    id BIGSERIAL PRIMARY KEY,

	part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    quilting_type TEXT NOT NULL,         -- Multi Needle
    design_ref TEXT NOT NULL,            -- Upload

    stitch_length_mm NUMERIC
        CHECK (stitch_length_mm > 0),

    pattern_repeat TEXT,                 -- Repeat Size / description

    wastage NUMERIC
        CHECK (wastage BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part2_quilting_advanced (
    id BIGSERIAL PRIMARY KEY,

    quilting_general_id BIGINT NOT NULL
        REFERENCES part2_quilting_general(id)
        ON DELETE CASCADE,

    variants TEXT,                       -- Quilting variants
    design TEXT NOT NULL,                -- Dropdown values
    needle_spacing NUMERIC
        CHECK (needle_spacing > 0),

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (quilting_general_id)
);

--Printing
CREATE TABLE part2_printing_general (
    id BIGSERIAL PRIMARY KEY,

	part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    printing_type TEXT NOT NULL,          -- Block Print
    design_ref TEXT NOT NULL,             -- Upload

    repeat_size TEXT,                     -- Block Size / Repeat Size

    wastage NUMERIC
        CHECK (wastage BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part2_printing_advanced (
    id BIGSERIAL PRIMARY KEY,

    printing_general_id BIGINT NOT NULL
        REFERENCES part2_printing_general(id)
        ON DELETE CASCADE,

    variants TEXT,                        -- Hand Block, Ajrakh, Dabu, etc.
    design TEXT NOT NULL,                 -- Dropdown designs

    screens SMALLINT
        CHECK (screens BETWEEN 1 AND 20),

    colors SMALLINT
        CHECK (colors > 0),

    coverage_percent NUMERIC
        CHECK (coverage_percent BETWEEN 0 AND 100),

    resolution TEXT,                      -- N/A or value

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (printing_general_id)
);

--Knitting
CREATE TABLE part2_knitting_general (
    id BIGSERIAL PRIMARY KEY,

	part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    machine_type TEXT NOT NULL,          -- Circular
    design_ref TEXT NOT NULL,            -- Upload

    gauge NUMERIC
        CHECK (gauge > 0),

    gsm NUMERIC
        CHECK (gsm > 0),

    wales_ratio NUMERIC(4,3)
        CHECK (wales_ratio BETWEEN 0 AND 1),

    courses_ratio NUMERIC(4,3)
        CHECK (courses_ratio BETWEEN 0 AND 1),

    wales_ratio_weight NUMERIC           -- Ratio / %age
        CHECK (wales_ratio_weight >= 0),

    courses_ratio_weight NUMERIC         -- Ratio / %age
        CHECK (courses_ratio_weight >= 0),

    wastage NUMERIC
        CHECK (wastage BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part2_knitting_advanced (
    id BIGSERIAL PRIMARY KEY,

    knitting_general_id BIGINT NOT NULL
        REFERENCES part2_knitting_general(id)
        ON DELETE CASCADE,

    design TEXT NOT NULL,                -- Dropdown knitting designs
    variants TEXT,                       -- Knit variants

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (knitting_general_id)
);

--Embroidery
CREATE TABLE part2_embroidery_general (
    id BIGSERIAL PRIMARY KEY,

	part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    machine_type TEXT NOT NULL,          -- Single Thread / Aari
    design_ref TEXT NOT NULL,            -- Upload

    wastage NUMERIC
        CHECK (wastage BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,      -- Buyer's / Initial / PP / Sample
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part2_embroidery_advanced (
    id BIGSERIAL PRIMARY KEY,

    embroidery_general_id BIGINT NOT NULL
        REFERENCES part2_embroidery_general(id)
        ON DELETE CASCADE,

    variants TEXT,                       -- Embroidery variants
    design TEXT NOT NULL,                -- Dropdown designs

    thread_colors SMALLINT
        CHECK (thread_colors > 0),

    stitch_count NUMERIC
        CHECK (stitch_count > 0),

    hoop_frame_size TEXT,                -- Frame size description

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (embroidery_general_id)
);

--Dyeing
CREATE TABLE part2_dyeing_general (
    id BIGSERIAL PRIMARY KEY,

	part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    dyeing_type TEXT NOT NULL,           -- Jigger / Jet / Beam / Pad
    color_reference TEXT NOT NULL,       -- Pantone / ARS / CSI / PMS
    reference_type TEXT NOT NULL,        -- Chip / Swatch / Physical / TPG / TDX

    reference_image TEXT NOT NULL,       -- Upload

    shrinkage_width_percent NUMERIC
        CHECK (shrinkage_width_percent BETWEEN 0 AND 100)
        NOT NULL,

    shrinkage_length_percent NUMERIC
        CHECK (shrinkage_length_percent BETWEEN 0 AND 100)
        NOT NULL,

    wastage NUMERIC
        CHECK (wastage BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part2_dyeing_advanced (
    id BIGSERIAL PRIMARY KEY,

    dyeing_general_id BIGINT NOT NULL
        REFERENCES part2_dyeing_general(id)
        ON DELETE CASCADE,

    variants TEXT,                       -- Polyester, Nylon, Acrylic, Blends

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (dyeing_general_id)
);

--Braiding
CREATE TABLE part2_braiding_general (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    machine_type TEXT NOT NULL,          -- Hand Braid
    design_ref TEXT NOT NULL,            -- Upload

    strand_count SMALLINT
        CHECK (strand_count > 0),

    width_or_diameter NUMERIC
        CHECK (width_or_diameter > 0),

    gsm NUMERIC
        CHECK (gsm > 0),

    wastage NUMERIC
        CHECK (wastage BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part2_braiding_advanced (
    id BIGSERIAL PRIMARY KEY,

    braiding_general_id BIGINT NOT NULL
        REFERENCES part2_braiding_general(id)
        ON DELETE CASCADE,

    variants TEXT,                       -- Multi-strand, Flat, Round, etc.
    design TEXT NOT NULL,                -- Strand/design dropdown
    pattern TEXT,                        -- Pattern name

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (braiding_general_id)
);

--Carpet
CREATE TABLE part2_carpet_general (
    id BIGSERIAL PRIMARY KEY,

    part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    machine_type TEXT NOT NULL,          -- Hand Knotted
    design_ref TEXT NOT NULL,            -- Upload

    gsm NUMERIC
        CHECK (gsm > 0),

    pile_height_mm NUMERIC
        CHECK (pile_height_mm > 0)
        NOT NULL,

    knot_type TEXT NOT NULL,             -- Dropdown

    tpi SMALLINT
        CHECK (tpi > 0),

    kpsi SMALLINT
        CHECK (kpsi > 0),

    pitch SMALLINT
        CHECK (pitch > 0),

    rows SMALLINT
        CHECK (rows > 0),

    wastage NUMERIC
        CHECK (wastage BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part2_carpet_advanced (
    id BIGSERIAL PRIMARY KEY,

    carpet_general_id BIGINT NOT NULL
        REFERENCES part2_carpet_general(id)
        ON DELETE CASCADE,

    variants TEXT,                       -- Dropdown variants
    design TEXT NOT NULL,                -- Dropdown designs

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (carpet_general_id)
);

--Cutting
CREATE TABLE part2_cutting_general (
    id BIGSERIAL PRIMARY KEY,

	part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    component_name VARCHAR(27),          -- Optional (if cutting per component)

    type TEXT NOT NULL,                  -- Scissor
    variants TEXT,                       -- Tailoring Scissor
    machine_type TEXT NOT NULL,          -- Dropdown (Scissor)

    wastage NUMERIC
        CHECK (wastage BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part2_cutting_advanced (
    id BIGSERIAL PRIMARY KEY,

    cutting_general_id BIGINT NOT NULL
        REFERENCES part2_cutting_general(id)
        ON DELETE CASCADE,

    cut_type TEXT NOT NULL,              -- Single Ply / Layered
    layers SMALLINT
        CHECK (layers > 0),

    nesting TEXT,                        -- Manual / Auto

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (cutting_general_id)
);

--Sewing
CREATE TABLE part2_sewing_general (
    id BIGSERIAL PRIMARY KEY,

	part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    spi SMALLINT
        CHECK (spi > 0),

    thread_type TEXT NOT NULL,           -- Spun Poly / Core Spun

    wastage NUMERIC
        CHECK (wastage BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part2_sewing_advanced (
    id BIGSERIAL PRIMARY KEY,

    sewing_general_id BIGINT NOT NULL
        REFERENCES part2_sewing_general(id)
        ON DELETE CASCADE,

    machine_type TEXT NOT NULL,          -- SNLS Machine
    stitch_type TEXT NOT NULL,           -- 301 Lockstitch
    variants TEXT,                       -- Dropdown
    needle_size TEXT,                    -- Text

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (sewing_general_id)
);

--fringe and tassels
CREATE TABLE part2_fringe_tassels_general (
    id BIGSERIAL PRIMARY KEY,

	part2_id BIGINT NOT NULL     
	REFERENCES part2_master(part2_id)     
	ON DELETE CASCADE,

    fringe_type TEXT NOT NULL,          -- dropdown
    material TEXT NOT NULL,             -- dropdown

    drop_length TEXT,                   -- dropdown / text
    tape_header_width TEXT,             -- dropdown / text

    colour TEXT,                        -- DTM / Multi / Iridescent / Ombre
    colour_reference TEXT,              -- upload reference image

    placement TEXT,
    placement_image TEXT,               -- upload reference image

    testing_requirements TEXT,          -- dropdown multiselect
    testing_document TEXT,              -- upload

    quantity_mode TEXT CHECK (quantity_mode IN ('PCS','LENGTH')),
    
    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part2_fringe_tassels_advance (
    id BIGSERIAL PRIMARY KEY,

    fringe_general_id BIGINT NOT NULL
        REFERENCES part2_fringe_tassels_general(id)
        ON DELETE CASCADE,

    finish TEXT,            -- dropdown
    attachment TEXT,        -- dropdown
    construction TEXT,      -- dropdown

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);
--PART 3 - ARTWORK AND LABELING
--COMMON DETAILS
CREATE TABLE part3_details (
    part3_detail_id BIGSERIAL PRIMARY KEY,
    product_id BIGINT REFERENCES products(product_id) ON DELETE CASCADE,
    section_id SMALLINT REFERENCES part3_sections(section_id),
    item_type TEXT NOT NULL,
    product_name TEXT NOT NULL,
    components TEXT NOT NULL
);

-- part 3 master table
CREATE TABLE part3_master (
    part3_id BIGSERIAL PRIMARY KEY,

    main_id BIGINT NOT NULL
        REFERENCES main_master(main_id)
        ON DELETE CASCADE,
		
    reference_code TEXT NOT NULL,
    remarks TEXT,

    status TEXT DEFAULT 'DRAFT',
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

--Brands labels
CREATE TABLE part3_brand_labels_general (
    id BIGSERIAL PRIMARY KEY,

    part3_id BIGINT NOT NULL     
	REFERENCES part3_master(part3_id)    
	ON DELETE CASCADE,


    label_type TEXT NOT NULL,             -- Dropdown / Others
    material TEXT NOT NULL,               -- Dropdown / Others

    artwork_ref TEXT,                     -- Upload (artwork spec)

    size_unit TEXT,                       -- mm / cm / inches
    width_mm NUMERIC
        CHECK (width_mm > 0),
    height_mm NUMERIC
        CHECK (height_mm > 0),

    placement TEXT,
    attachment TEXT,

    testing_requirements TEXT,            -- Dropdown / multiselect

    quantity_type TEXT,                   -- Pieces / Running Length
    quantity_value NUMERIC
        CHECK (quantity_value > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,       -- Buyer / Initial / IPP / Woven Sample
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part3_brand_labels_advanced (
    id BIGSERIAL PRIMARY KEY,

    label_general_id BIGINT NOT NULL
        REFERENCES part3_brand_labels_general(id)
        ON DELETE CASCADE,

    fold_type TEXT,                       -- Dropdown / Others
    weave_density TEXT,                   -- Dropdown / Others
    thread_type TEXT,                     -- Dropdown / Others
    colours TEXT,                         -- Dropdown / Others
    background TEXT,                      -- Dropdown / Others
    finishing TEXT,                       -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (label_general_id)
);

--Care Labels
CREATE TABLE part3_care_labels_general (
    id BIGSERIAL PRIMARY KEY,

    part3_id BIGINT NOT NULL     
	REFERENCES part3_master(part3_id)     
	ON DELETE CASCADE,


    label_type TEXT NOT NULL,             -- Dropdown / Others
    material TEXT NOT NULL,               -- Dropdown / Others

    artwork_ref TEXT,                     -- Upload (artwork spec)

    size_unit TEXT,                       -- mm / cm / inches
    width_mm NUMERIC
        CHECK (width_mm > 0),
    length_mm NUMERIC
        CHECK (length_mm > 0),

    placement TEXT,

    testing_requirements TEXT NOT NULL,   -- Multiselect / text

    quantity_type TEXT,                   -- Pieces / Running Length
    quantity_value NUMERIC
        CHECK (quantity_value > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,       -- Buyer / Initial / IPP / Text Compliance
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part3_care_labels_advanced (
    id BIGSERIAL PRIMARY KEY,

    care_label_general_id BIGINT NOT NULL
        REFERENCES part3_care_labels_general(id)
        ON DELETE CASCADE,

    print_type TEXT,                      -- Dropdown / Others
    ink_type TEXT,                        -- Dropdown / Others
    manufacturer_id TEXT,                 -- Dropdown / Others
    permanence TEXT,                      -- Dropdown / Others
    language TEXT,                        -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (care_label_general_id)
);

--Special tags
CREATE TABLE part3_special_tags_general (
    id BIGSERIAL PRIMARY KEY,

    part3_id BIGINT NOT NULL     
	REFERENCES part3_master(part3_id)     
	ON DELETE CASCADE,


    tag_type TEXT NOT NULL,               -- Dropdown / Others
    material TEXT NOT NULL,               -- Dropdown / Others

    artwork_ref TEXT,                     -- Upload (artwork spec)

    size_unit TEXT,                       -- mm / cm / inches
    width_mm NUMERIC
        CHECK (width_mm > 0),
    height_mm NUMERIC
        CHECK (height_mm > 0),

    attachment TEXT NOT NULL,             -- Dropdown / Others
    finishing TEXT NOT NULL,              -- Dropdown / Others

    placement TEXT,                       -- Text
    placement_image_ref TEXT,             -- Upload reference image

    testing_requirements TEXT NOT NULL,   -- Multiselect / text

    quantity_type TEXT,                   -- PCS / Running Length
    quantity_value NUMERIC
        CHECK (quantity_value > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,       -- Buyer / Initial / IPP / Design Proof
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part3_special_tags_advanced (
    id BIGSERIAL PRIMARY KEY,

    special_tag_general_id BIGINT NOT NULL
        REFERENCES part3_special_tags_general(id)
        ON DELETE CASCADE,

    colours TEXT,                         -- Dropdown / Others
    printing TEXT,                        -- Dropdown / Others
    seal_type TEXT,                       -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (special_tag_general_id)
);

--Safety Labels
CREATE TABLE part3_safety_labels_general (
    id BIGSERIAL PRIMARY KEY,

    part3_id BIGINT NOT NULL     
	REFERENCES part3_master(part3_id)     
	ON DELETE CASCADE,


    label_type TEXT NOT NULL,             -- Dropdown / Others
    material TEXT NOT NULL,               -- Dropdown / Others

    artwork_ref TEXT,                     -- Upload (artwork spec)

    size_unit TEXT,                       -- mm / cm / inches
    width_mm NUMERIC
        CHECK (width_mm > 0),
    height_mm NUMERIC
        CHECK (height_mm > 0),

    placement TEXT,
    placement_image_ref TEXT,             -- Upload image reference

    testing_requirements TEXT NOT NULL,   -- Multiselect / text

    quantity_pieces NUMERIC
        CHECK (quantity_pieces > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part3_safety_labels_advanced (
    id BIGSERIAL PRIMARY KEY,

    safety_label_general_id BIGINT NOT NULL
        REFERENCES part3_safety_labels_general(id)
        ON DELETE CASCADE,

    regulation TEXT,                      -- Dropdown / Others
    font_size TEXT,                       -- Dropdown / Others
    permanence TEXT,                      -- Dropdown / Others
    symbol TEXT,                          -- Dropdown / Others
    ink_durability TEXT,                  -- Dropdown / Others
    certification_id TEXT,                -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (safety_label_general_id)
);

--RFID
CREATE TABLE part3_rfid_tags_general (
    id BIGSERIAL PRIMARY KEY,

    part3_id BIGINT NOT NULL     
	REFERENCES part3_master(part3_id)     
	ON DELETE CASCADE,

    section_id SMALLINT NOT NULL
        REFERENCES part3_sections(section_id),

    tag_type TEXT NOT NULL,               -- Dropdown / Others
    form_factor TEXT NOT NULL,            -- Dropdown / Others

    artwork_ref TEXT,                     -- Upload (artwork spec)

    chip_model TEXT NOT NULL,             -- Dropdown / Others

    size_unit TEXT,                       -- mm / cm / inches
    width_mm NUMERIC
        CHECK (width_mm > 0),
    height_mm NUMERIC
        CHECK (height_mm > 0),

    placement TEXT,
    placement_image_ref TEXT,             -- Upload image reference

    testing_requirements TEXT NOT NULL,   -- Multiselect / upload ref

    quantity_pieces NUMERIC
        CHECK (quantity_pieces > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100)
        NOT NULL,

    approval_ref TEXT NOT NULL,            -- Upload
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part3_rfid_tags_advanced (
    id BIGSERIAL PRIMARY KEY,

    rfid_tag_general_id BIGINT NOT NULL
        REFERENCES part3_rfid_tags_general(id)
        ON DELETE CASCADE,

    coding TEXT,                          -- Dropdown / Others
    encoding_standard TEXT,               -- Dropdown / Others
    security TEXT,                        -- Dropdown / Others
    memory TEXT,                          -- Dropdown / Others
    chip_frequency TEXT,                  -- Dropdown / Others
    adhesive TEXT,                        -- Dropdown / Others
    read_range TEXT,                      -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (rfid_tag_general_id)
);

--Law labels
CREATE TABLE part3_law_labels_general (
    id BIGSERIAL PRIMARY KEY,

    part3_id BIGINT NOT NULL     
	REFERENCES part3_master(part3_id)     
	ON DELETE CASCADE,


    label_type TEXT NOT NULL,             -- Dropdown / Others
    material TEXT NOT NULL,               -- Dropdown / Others

    artwork_ref TEXT,                     -- Upload (artwork spec)

    size_unit TEXT,                       -- mm / cm / inches
    width_mm NUMERIC
        CHECK (width_mm > 0),
    height_mm NUMERIC
        CHECK (height_mm > 0),

    placement TEXT,
    placement_image_ref TEXT,             -- Upload image reference

    testing_requirements TEXT NOT NULL,   -- Dropdown / multiselect

    quantity_pieces NUMERIC
        CHECK (quantity_pieces > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part3_law_labels_advanced (
    id BIGSERIAL PRIMARY KEY,

    law_label_general_id BIGINT NOT NULL
        REFERENCES part3_law_labels_general(id)
        ON DELETE CASCADE,

    permanence TEXT,                      -- Dropdown / Others
    font_text_size TEXT,                  -- Dropdown / Others
    content_mandates TEXT NOT NULL,       -- Legal text requirements
    filling_materials TEXT,               -- Dropdown / Others
    new_used_status TEXT,                 -- Dropdown / Others
    registration_licenses TEXT,           -- Dropdown / Others
    rn_ca_number TEXT,                    -- Dropdown / Others
    state_requirements TEXT,              -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (law_label_general_id)
);

--Hangtag seals
CREATE TABLE part3_hang_seals_general (
    id BIGSERIAL PRIMARY KEY,

    part3_id BIGINT NOT NULL     
	REFERENCES part3_master(part3_id)     
	ON DELETE CASCADE,


    seal_type TEXT NOT NULL,              -- Dropdown / Others
    material TEXT NOT NULL,               -- Dropdown / Others

    artwork_ref TEXT,                     -- Upload (artwork spec)

    size_unit TEXT,                       -- mm / cm / inches
    width_mm NUMERIC
        CHECK (width_mm > 0),
    height_mm NUMERIC
        CHECK (height_mm > 0),

    placement TEXT,
    placement_image_ref TEXT,             -- Upload image reference

    testing_requirements TEXT NOT NULL,   -- Dropdown / multiselect

    quantity_pieces NUMERIC
        CHECK (quantity_pieces > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part3_hang_seals_advanced (
    id BIGSERIAL PRIMARY KEY,

    hang_seal_general_id BIGINT NOT NULL
        REFERENCES part3_hang_seals_general(id)
        ON DELETE CASCADE,

    fastening TEXT,                       -- Dropdown / Others
    pre_stringing TEXT,                   -- Dropdown / Others
    string_finish TEXT,                   -- Dropdown / Others
    seal_shape TEXT,                      -- Dropdown / Others
    colour TEXT,                          -- Dropdown / Others
    logo_branding TEXT,                   -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (hang_seal_general_id)
);

--Price tags
CREATE TABLE part3_price_tags_general (
    id BIGSERIAL PRIMARY KEY,

    part3_id BIGINT NOT NULL     
	REFERENCES part3_master(part3_id)     
	ON DELETE CASCADE,


    tag_type TEXT NOT NULL,               -- Dropdown / Others
    material TEXT NOT NULL,               -- Dropdown / Others

    artwork_ref TEXT,                     -- Upload (artwork spec)

    size_unit TEXT,                       -- mm / cm / inches
    width_mm NUMERIC
        CHECK (width_mm > 0),
    height_mm NUMERIC
        CHECK (height_mm > 0),

    placement TEXT,
    placement_image_ref TEXT,             -- Upload image reference

    testing_requirements TEXT NOT NULL,   -- Dropdown / multiselect

    quantity_type TEXT,                   -- Pieces / Rolls
    quantity_value NUMERIC
        CHECK (quantity_value > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part3_price_tags_advanced (
    id BIGSERIAL PRIMARY KEY,

    price_tag_general_id BIGINT NOT NULL
        REFERENCES part3_price_tags_general(id)
        ON DELETE CASCADE,

    barcode_type TEXT,                    -- Dropdown / Others
    barcode_quality TEXT,                 -- Dropdown / Others
    print_method TEXT,                    -- Dropdown / Others
    variable_data TEXT,                   -- Dropdown / Others
    content TEXT,                         -- Price / SKU / MRP logic
    currency TEXT,                        -- Dropdown / Others
    gumming_quality TEXT,                 -- Dropdown / Others
    finish TEXT,                          -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (price_tag_general_id)
);

--heat transfer
CREATE TABLE part3_heat_transfer_general (
    id BIGSERIAL PRIMARY KEY,

    part3_id BIGINT NOT NULL     
	REFERENCES part3_master(part3_id)    
	ON DELETE CASCADE,


    transfer_type TEXT NOT NULL,          -- Dropdown / Others
    material_base TEXT NOT NULL,           -- Dropdown / Others

    artwork_ref TEXT,                     -- Upload / reference image

    size_unit TEXT,                       -- mm / cm / inches
    width_mm NUMERIC
        CHECK (width_mm > 0),
    height_mm NUMERIC
        CHECK (height_mm > 0),

    placement TEXT,
    placement_image_ref TEXT,             -- Upload image reference

    testing_requirements TEXT NOT NULL,   -- Dropdown / multiselect

    quantity_type TEXT,                   -- Pieces / Sheets / Rolls
    quantity_value NUMERIC
        CHECK (quantity_value > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part3_heat_transfer_advanced (
    id BIGSERIAL PRIMARY KEY,

    heat_transfer_general_id BIGINT NOT NULL
        REFERENCES part3_heat_transfer_general(id)
        ON DELETE CASCADE,

    ink_type TEXT,                        -- Dropdown / Others
    fabric_compatibility TEXT,            -- Dropdown / Others
    application_spec TEXT,                -- Dropdown / Others
    peel_type TEXT,                       -- Dropdown / Others
    finish_hand_feel TEXT,                -- Dropdown / Others
    stretch TEXT,                         -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (heat_transfer_general_id)
);

--upc labels
CREATE TABLE part3_upc_labels_general (
    id BIGSERIAL PRIMARY KEY,

    part3_id BIGINT NOT NULL  
	REFERENCES part3_master(part3_id)  
	ON DELETE CASCADE,


    label_type TEXT NOT NULL,             -- Dropdown / Others
    material TEXT NOT NULL,               -- Dropdown / Others

    artwork_ref TEXT,                     -- Upload (artwork spec)

    size_unit TEXT,                       -- mm / cm / inches
    width_mm NUMERIC
        CHECK (width_mm > 0),
    height_mm NUMERIC
        CHECK (height_mm > 0),

    placement TEXT,
    placement_image_ref TEXT,             -- Upload image reference

    testing_requirements TEXT NOT NULL,   -- Dropdown / multiselect

    quantity_type TEXT,                   -- Pieces / Rolls
    quantity_value NUMERIC
        CHECK (quantity_value > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part3_upc_labels_advanced (
    id BIGSERIAL PRIMARY KEY,

    upc_label_general_id BIGINT NOT NULL
        REFERENCES part3_upc_labels_general(id)
        ON DELETE CASCADE,

    quality TEXT,                         -- Dropdown / Others
    quiet_zone TEXT,                     -- Dropdown / Others
    barcode_standard TEXT,               -- UPC-A / UPC-E / EAN, etc.
    print_method TEXT,                   -- Dropdown / Others
    variable_data TEXT,                  -- Yes / No / Type
    gumming_quality TEXT,                -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (upc_label_general_id)
);

--size labels
CREATE TABLE part3_size_labels_general (
    id BIGSERIAL PRIMARY KEY,

    part3_id BIGINT NOT NULL   
	REFERENCES part3_master(part3_id)  
	ON DELETE CASCADE,


    label_type TEXT NOT NULL,             -- Dropdown / Others
    material TEXT NOT NULL,               -- Dropdown / Others

    artwork_ref TEXT,                     -- Upload (artwork spec)

    size_unit TEXT,                       -- mm / cm / inches
    width_mm NUMERIC
        CHECK (width_mm > 0),
    height_mm NUMERIC
        CHECK (height_mm > 0),

    size_system TEXT,                     -- Dropdown / Others
    size_code TEXT,                       -- S / M / L / 32 / EU / etc.
    fold_type TEXT,                       -- Dropdown / Others

    placement TEXT,
    placement_image_ref TEXT,             -- Upload image reference

    testing_requirements TEXT NOT NULL,   -- Dropdown / multiselect

    quantity_type TEXT,                   -- Pieces / Rolls
    quantity_value NUMERIC
        CHECK (quantity_value > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part3_size_labels_advanced (
    id BIGSERIAL PRIMARY KEY,

    size_label_general_id BIGINT NOT NULL
        REFERENCES part3_size_labels_general(id)
        ON DELETE CASCADE,

    accuracy TEXT,                        -- Dropdown / Others
    bundling TEXT,                        -- Dropdown / Others
    colour TEXT,                          -- Dropdown / Others
    font TEXT,                            -- Dropdown / Others
    finish TEXT,                          -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (size_label_general_id)
);

--anti-counterfeit
CREATE TABLE part3_anti_counterfeit_general (
    id BIGSERIAL PRIMARY KEY,

    part3_id BIGINT NOT NULL  
	REFERENCES part3_master(part3_id) 
	ON DELETE CASCADE,


    label_type TEXT NOT NULL,             -- Dropdown / Others
    material TEXT NOT NULL,               -- Dropdown / Others

    artwork_ref TEXT,                     -- Upload (artwork spec)

    size_unit TEXT,                       -- mm / cm / inches
    width_mm NUMERIC
        CHECK (width_mm > 0),
    height_mm NUMERIC
        CHECK (height_mm > 0),

    security_feature TEXT NOT NULL,       -- Dropdown / Others
    hologram_type TEXT NOT NULL,           -- Dropdown / Others
    numbering TEXT,                       -- Dropdown / Others

    placement TEXT,
    placement_image_ref TEXT,             -- Upload image reference

    testing_requirements TEXT NOT NULL,   -- Dropdown / multiselect

    quantity_pieces NUMERIC
        CHECK (quantity_pieces > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part3_anti_counterfeit_advanced (
    id BIGSERIAL PRIMARY KEY,

    anti_counterfeit_general_id BIGINT NOT NULL
        REFERENCES part3_anti_counterfeit_general(id)
        ON DELETE CASCADE,

    verification TEXT,                    -- Dropdown / Others
    qr_code_content TEXT,                 -- Dropdown / Others
    application TEXT,                     -- Dropdown / Others
    tamper_evidence TEXT,                 -- Dropdown / Others
    database TEXT,                        -- Dropdown / Others
    gumming_quality TEXT,                 -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (anti_counterfeit_general_id)
);

--QC labels
CREATE TABLE part3_qc_labels_general (
    id BIGSERIAL PRIMARY KEY,

    part3_id BIGINT NOT NULL  
	REFERENCES part3_master(part3_id) 
	ON DELETE CASCADE,


    label_type TEXT NOT NULL,             -- Dropdown / Others
    material TEXT NOT NULL,               -- Dropdown / Others

    artwork_ref TEXT,                     -- Upload (artwork spec)

    size_unit TEXT,                       -- mm / cm / inches
    width_mm NUMERIC
        CHECK (width_mm > 0),
    height_mm NUMERIC
        CHECK (height_mm > 0),

    content TEXT NOT NULL,                -- Dropdown / Others
    coding_system TEXT,                   -- Dropdown / Others
    gumming_quality TEXT,                 -- Dropdown / Others

    placement TEXT,
    placement_image_ref TEXT,             -- Upload image reference

    testing_requirements TEXT NOT NULL,   -- Dropdown / multiselect

    quantity_pieces NUMERIC
        CHECK (quantity_pieces > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part3_qc_labels_advanced (
    id BIGSERIAL PRIMARY KEY,

    qc_label_general_id BIGINT NOT NULL
        REFERENCES part3_qc_labels_general(id)
        ON DELETE CASCADE,

    application TEXT,                     -- Dropdown / Others
    timing TEXT,                          -- HOLD / Inline / Post-process
    removal TEXT,                         -- Dropdown / Others
    traceability TEXT,                    -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (qc_label_general_id)
);

--belly bands
CREATE TABLE part3_belly_bands_general (
    id BIGSERIAL PRIMARY KEY,

    part3_id BIGINT NOT NULL   
	REFERENCES part3_master(part3_id)    
	ON DELETE CASCADE,


    band_type TEXT NOT NULL,              -- Dropdown / Others
    material TEXT NOT NULL,               -- Dropdown / Others

    artwork_ref TEXT,                     -- Upload (artwork spec)

    size_unit TEXT,                       -- mm / cm / inches
    width_mm NUMERIC
        CHECK (width_mm > 0),
    height_mm NUMERIC
        CHECK (height_mm > 0),

    closure TEXT NOT NULL,                -- Dropdown / Others

    placement TEXT,
    placement_image_ref TEXT,             -- Upload image reference

    testing_requirements TEXT NOT NULL,   -- Dropdown / multiselect

    quantity_pieces NUMERIC
        CHECK (quantity_pieces > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part3_belly_bands_advanced (
    id BIGSERIAL PRIMARY KEY,

    belly_band_general_id BIGINT NOT NULL
        REFERENCES part3_belly_bands_general(id)
        ON DELETE CASCADE,

    product_fit TEXT,                     -- Dropdown / Others
    printing TEXT,                        -- Dropdown / Others
    fold_lines TEXT,                      -- Dropdown / Others
    durability TEXT,                      -- Dropdown / Others
    content TEXT,                         -- Dropdown / Others
    colours TEXT,                         -- Dropdown / Others
    finish TEXT,                          -- Dropdown / Others
    die_cut TEXT,                         -- Dropdown / Others
    gumming_quality TEXT,                 -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (belly_band_general_id)
);

--insert cards
CREATE TABLE part3_insert_cards_general (
    id BIGSERIAL PRIMARY KEY,

    part3_id BIGINT NOT NULL   
	REFERENCES part3_master(part3_id)  
	ON DELETE CASCADE,


    card_type TEXT NOT NULL,              -- Dropdown / Others
    material TEXT NOT NULL,               -- Dropdown / Others

    artwork_ref TEXT,                     -- Upload (artwork spec)

    size_unit TEXT,                       -- mm / cm / inches
    width_mm NUMERIC
        CHECK (width_mm > 0),
    height_mm NUMERIC
        CHECK (height_mm > 0),

    placement TEXT,
    placement_image_ref TEXT,             -- Upload image reference

    testing_requirements TEXT NOT NULL,   -- Dropdown / multiselect

    quantity_pieces NUMERIC
        CHECK (quantity_pieces > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part3_insert_cards_advanced (
    id BIGSERIAL PRIMARY KEY,

    insert_card_general_id BIGINT NOT NULL
        REFERENCES part3_insert_cards_general(id)
        ON DELETE CASCADE,

    function TEXT,                        -- Dropdown / Others
    content TEXT,                         -- Dropdown / Others
    printing TEXT,                        -- Dropdown / Others
    finish TEXT,                          -- Dropdown / Others
    stiffness TEXT,                       -- Dropdown / Others
    acid_free TEXT,                       -- Yes / No / Spec
    branding TEXT,                        -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (insert_card_general_id)
);


--ribbons
CREATE TABLE part3_ribbons_general (
    id BIGSERIAL PRIMARY KEY,

    part3_id BIGINT NOT NULL  
	REFERENCES part3_master(part3_id) 
	ON DELETE CASCADE,


    ribbon_type TEXT NOT NULL,            -- Dropdown / Others
    material TEXT NOT NULL,               -- Dropdown / Others

    artwork_ref TEXT,                     -- Upload (print / logo ref)

    width_mm NUMERIC
        CHECK (width_mm > 0),             -- Ribbon width

    roll_length TEXT,                     -- Dropdown / Others (optional)

    testing_requirements TEXT NOT NULL,   -- Dropdown / multiselect

    quantity_type TEXT,                   -- R LENGTH / ROLLS / KGS / PCS
    quantity_value NUMERIC
        CHECK (quantity_value > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100)
        NOT NULL,

    approval_against TEXT NOT NULL,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part3_ribbons_advanced (
    id BIGSERIAL PRIMARY KEY,

    ribbon_general_id BIGINT NOT NULL
        REFERENCES part3_ribbons_general(id)
        ON DELETE CASCADE,

    colour TEXT,                          -- Dropdown / Others
    finish TEXT,                          -- Dropdown / Others
    edge_type TEXT,                       -- Dropdown / Others
    print TEXT,                           -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (ribbon_general_id)
);

--PART 4 - PACKAGING
--COMMON DETAILS
CREATE TABLE part4_details (
    part4_detail_id BIGSERIAL PRIMARY KEY,
    product_id BIGINT REFERENCES products(product_id) ON DELETE CASCADE,
	to_be_shipped TEXT NOT NULL,
	select_product TEXT NOT NULL,
	master_pack TEXT NOT NULL,
    casepack_quantity INTEGER NOT NULL
);

--SIZE 
CREATE TABLE part4_size (
    part4_size_id BIGSERIAL PRIMARY KEY,
    product_id BIGINT REFERENCES products(product_id) ON DELETE CASCADE,
    width NUMERIC CHECK (width >= 0) NOT NULL,
    length NUMERIC CHECK (length >= 0) NOT NULL,
    height NUMERIC CHECK (height >= 0) NOT NULL,
    unit TEXT NOT NULL
);
-- part 4 master table
CREATE TABLE part4_master (
    part4_id BIGSERIAL PRIMARY KEY,

    main_id BIGINT NOT NULL
        REFERENCES main_master(main_id)
        ON DELETE CASCADE,
		
    reference_code TEXT NOT NULL,
    remarks TEXT,

    status TEXT DEFAULT 'DRAFT',
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

--Carton Boxes
CREATE TABLE part4_carton_boxes_general (
    id BIGSERIAL PRIMARY KEY,

    

    part4_id BIGINT NOT NULL     
	REFERENCES part4_master(part4_id)     
	ON DELETE CASCADE,

    casepack NUMERIC
        CHECK (casepack > 0),

    packaging_type TEXT,                  -- Standard / Assorted / PC

    carton_type TEXT NOT NULL,             -- Dropdown / Others
    ply_count TEXT,                        -- Dropdown / Others
    board_grade TEXT,                      -- Dropdown / Others
    joint_type TEXT,                       -- Dropdown / Others

    bursting_strength NUMERIC
        CHECK (bursting_strength > 0),     -- lbs / kg / cm2

    length_cm NUMERIC
        CHECK (length_cm > 0),
    width_cm NUMERIC
        CHECK (width_cm > 0),
    height_cm NUMERIC
        CHECK (height_cm > 0),

    stiffener_required BOOLEAN,
    stiffener_length_cm NUMERIC
        CHECK (stiffener_length_cm > 0),
    stiffener_width_cm NUMERIC
        CHECK (stiffener_width_cm > 0),
    stiffener_height_cm NUMERIC
        CHECK (stiffener_height_cm > 0),

    testing_requirements_ref TEXT,         -- Upload

    quantity_pieces NUMERIC
        CHECK (quantity_pieces > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part4_carton_boxes_advanced (
    id BIGSERIAL PRIMARY KEY,

    carton_box_general_id BIGINT NOT NULL
        REFERENCES part4_carton_boxes_general(id)
        ON DELETE CASCADE,

    artwork_ref TEXT,                     -- Upload
    paper_gsm TEXT,                       -- Dropdown / Others
    flute_type TEXT,                      -- Dropdown / Others
    ect TEXT,                             -- Edge Crush Test
    printing TEXT,                        -- Dropdown / Others
    print_content TEXT,                   -- Dropdown / Others
    print_colours TEXT,                   -- Dropdown / Others
    coating_treatment TEXT,               -- Dropdown / Others
    hand_holes TEXT,                      -- Yes / No / Spec
    certification TEXT,                   -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (carton_box_general_id)
);

--Tape
CREATE TABLE part4_tapes_general (
    id BIGSERIAL PRIMARY KEY,

    

    part4_id BIGINT NOT NULL     
	REFERENCES part4_master(part4_id)     
	ON DELETE CASCADE,

    tape_type TEXT NOT NULL,                 -- Dropdown / Others
    material TEXT NOT NULL,                  -- Dropdown / Others

    gauge_micron NUMERIC
        CHECK (gauge_micron > 0),

    width_mm NUMERIC
        CHECK (width_mm > 0),

    length_value NUMERIC
        CHECK (length_value > 0),            -- meters / yards

    length_unit TEXT,                        -- m / yards

    gumming_quality TEXT,                    -- Dropdown / Others

    application TEXT,                        -- 6 ways, round about, etc.

    testing_requirements_ref TEXT,           -- Upload

    quantity_type TEXT NOT NULL,             -- Rolls / Cases
    quantity_value NUMERIC
        CHECK (quantity_value > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part4_tapes_advanced (
    id BIGSERIAL PRIMARY KEY,

    tape_general_id BIGINT NOT NULL
        REFERENCES part4_tapes_general(id)
        ON DELETE CASCADE,

    colour TEXT,                             -- Dropdown / Others
    adhesive_type TEXT,                     -- Dropdown / Others
    artwork_ref TEXT,                       -- Upload
    printing TEXT,                          -- Dropdown / Others
    print_repeat TEXT,                      -- Dropdown / Others

    core_size TEXT,                         -- e.g. 3" core
    noise_level TEXT,                       -- Dropdown / Others
    temperature_range TEXT,                 -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (tape_general_id)
);

--Foam insert
CREATE TABLE part4_foam_inserts_general (
    id BIGSERIAL PRIMARY KEY,

    

    part4_id BIGINT NOT NULL     
	REFERENCES part4_master(part4_id)     
	ON DELETE CASCADE,

    foam_type TEXT NOT NULL,              -- Dropdown / Others
    material TEXT NOT NULL,               -- Dropdown / Others

    density_kg_m3 NUMERIC
        CHECK (density_kg_m3 > 0),

    thickness_cm NUMERIC
        CHECK (thickness_cm > 0),

    length_cm NUMERIC
        CHECK (length_cm > 0),
    width_cm NUMERIC
        CHECK (width_cm > 0),
    height_cm NUMERIC
        CHECK (height_cm > 0),

    colour TEXT,                          -- White, Black, Pink (AS), Blue, Custom

    quantity_pcs NUMERIC
        CHECK (quantity_pcs > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part4_foam_inserts_advanced (
    id BIGSERIAL PRIMARY KEY,

    foam_insert_general_id BIGINT NOT NULL
        REFERENCES part4_foam_inserts_general(id)
        ON DELETE CASCADE,

    cavity_cutout TEXT,                  -- Yes / CNC / Die-cut / Custom
    anti_static TEXT,                    -- Yes / No / Grade
    lamination TEXT,                     -- Yes / Type / Material

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (foam_insert_general_id)
);

--Pallet Strap
CREATE TABLE part4_pallet_straps_general (
    id BIGSERIAL PRIMARY KEY,

    

    part4_id BIGINT NOT NULL     
	REFERENCES part4_master(part4_id)     
	ON DELETE CASCADE,

    strap_type TEXT NOT NULL,              -- Dropdown / Others
    application TEXT,                      -- Dropdown / Others

    width_cm NUMERIC
        CHECK (width_cm > 0),

    seal_type TEXT,                        -- Dropdown / Others
    seal_size_cm NUMERIC
        CHECK (seal_size_cm > 0),

    colour TEXT,                           -- Dropdown / Others

    quantity_meters NUMERIC
        CHECK (quantity_meters > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part4_pallet_straps_advanced (
    id BIGSERIAL PRIMARY KEY,

    pallet_strap_general_id BIGINT NOT NULL
        REFERENCES part4_pallet_straps_general(id)
        ON DELETE CASCADE,

    tensile_strength_kg NUMERIC
        CHECK (tensile_strength_kg > 0),   -- 150–500+

    core_size_mm NUMERIC
        CHECK (core_size_mm > 0),          -- 200 / 400 / 406

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (pallet_strap_general_id)
);

--Polybag Bale
CREATE TABLE part4_bale_general (
    id BIGSERIAL PRIMARY KEY,

    

    part4_id BIGINT NOT NULL     
	REFERENCES part4_master(part4_id)     
	ON DELETE CASCADE,

    film_type TEXT NOT NULL,               -- Dropdown / Others
    material TEXT NOT NULL,                -- Dropdown / Others

    gauge_gsm TEXT,                        -- Gauge or GSM (as per UI)

    roll_width NUMERIC
        CHECK (roll_width > 0),

    roll_width_unit TEXT,                  -- inch / cm

    colour TEXT,                           -- Dropdown / Others

    testing_requirements_ref TEXT,         -- Upload

    quantity_type TEXT NOT NULL,            -- Rolls / Kg
    quantity_value NUMERIC
        CHECK (quantity_value > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part4_bale_advanced (
    id BIGSERIAL PRIMARY KEY,

    film_general_id BIGINT NOT NULL
        REFERENCES part4_bale_general(id)
        ON DELETE CASCADE,

    artwork_ref TEXT,                      -- Upload
    printing TEXT,                         -- Dropdown / Others
    core_size TEXT,                        -- Dropdown / Others
    perforation TEXT,                      -- Yes / Type
    cling_tack TEXT,                       -- Dropdown / Others
    uv_stabilized TEXT,                    -- Yes / No / Grade
    anti_static TEXT,                      -- Yes / No / Grade

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (film_general_id)
);

--Polybag
CREATE TABLE part4_polybags_general (
    id BIGSERIAL PRIMARY KEY,

    

    part4_id BIGINT NOT NULL     
	REFERENCES part4_master(part4_id)     
	ON DELETE CASCADE,

    bag_type TEXT NOT NULL,                 -- Dropdown / Others
    material TEXT NOT NULL,                 -- Dropdown / Others

    gauge_micron NUMERIC
        CHECK (gauge_micron > 0),

    width_cm NUMERIC
        CHECK (width_cm > 0),
    length_cm NUMERIC
        CHECK (length_cm > 0),
    gusset_cm NUMERIC
        CHECK (gusset_cm >= 0),

    flap_required BOOLEAN,

    flap_length_cm NUMERIC
        CHECK (flap_length_cm > 0),
    flap_width_cm NUMERIC
        CHECK (flap_width_cm > 0),
    flap_height_cm NUMERIC
        CHECK (flap_height_cm > 0),

    testing_requirements_ref TEXT,          -- Upload

    quantity_type TEXT NOT NULL,            -- pcs / kg
    quantity_value NUMERIC
        CHECK (quantity_value > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part4_polybags_advanced (
    id BIGSERIAL PRIMARY KEY,

    polybag_general_id BIGINT NOT NULL
        REFERENCES part4_polybags_general(id)
        ON DELETE CASCADE,

    seal_type TEXT,                         -- Dropdown / Others
    vent_holes TEXT,                        -- Yes / No / Count / Spec
    suffocation_warning BOOLEAN,

    artwork_ref TEXT,                      -- Upload
    printing TEXT,                         -- Dropdown / Others
    print_colour TEXT,                     -- Black / White / Pantone / Custom
    print_position_ref TEXT,               -- Upload image reference

    anti_static TEXT,                      -- Yes / No / Grade
    food_grade TEXT,                       -- Yes / No / Standard
    recyclable TEXT,                       -- Yes / No / Type
    clarity TEXT,                          -- Dropdown / Others

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (polybag_general_id)
);

--Silica gel
CREATE TABLE part4_desiccants_general (
    id BIGSERIAL PRIMARY KEY,

    

    part4_id BIGINT NOT NULL     
	REFERENCES part4_master(part4_id)     
	ON DELETE CASCADE,

    desiccant_type TEXT NOT NULL,           -- Dropdown / Others
    form TEXT NOT NULL,                     -- Beads / Clay / Gel etc.

    unit_size_grams NUMERIC
        CHECK (unit_size_grams > 0),

    colour TEXT,                            -- Dropdown / Others

    placement TEXT,
    placement_image_ref TEXT,               -- Upload image reference

    quantity_pcs NUMERIC
        CHECK (quantity_pcs > 0),

    casepack_logic TEXT,                    -- e.g. X pcs per carton / pallet

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,                  -- Buyer / QA
    remarks TEXT,                           -- e.g. HIC card if required

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part4_desiccants_advanced (
    id BIGSERIAL PRIMARY KEY,

    desiccant_general_id BIGINT NOT NULL
        REFERENCES part4_desiccants_general(id)
        ON DELETE CASCADE,

    absorption_capacity TEXT,               -- Dropdown / Others
    indicating_type TEXT,                   -- Yes / No / Type
    packet_material TEXT,                   -- Dropdown / Others
    packet_size TEXT,                       -- Dropdown / Others
    food_safe TEXT,                         -- Yes / No / Standard

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (desiccant_general_id)
);

--Stretch Wrap
CREATE TABLE part4_stretch_wrap_general (
    id BIGSERIAL PRIMARY KEY,

    

    part4_id BIGINT NOT NULL 
	REFERENCES part4_master(part4_id)     
	ON DELETE CASCADE,

    wrap_type TEXT NOT NULL,               -- Dropdown / Others
    material TEXT NOT NULL,                -- LLDPE, etc.

    width_cm NUMERIC
        CHECK (width_cm > 0),

    thickness_gauge TEXT,                  -- Gauge / Micron (UI-driven)

    cling TEXT,                            -- Dropdown / Others
    colour TEXT,                           -- Dropdown / Others

    quantity_rolls NUMERIC
        CHECK (quantity_rolls > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE part4_stretch_wrap_advanced (
    id BIGSERIAL PRIMARY KEY,

    stretch_wrap_general_id BIGINT NOT NULL
        REFERENCES part4_stretch_wrap_general(id)
        ON DELETE CASCADE,

    stretch_percent TEXT,                  -- Dropdown / Others (e.g. 150%, 200%)
    core_size_cm NUMERIC
        CHECK (core_size_cm > 0),

    uv_stabilized TEXT,                    -- Yes / No / Grade
    vci_anti_corrosion TEXT,               -- Yes / No / Type

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),

    UNIQUE (stretch_wrap_general_id)
);

--Corner Protector
CREATE TABLE part4_corner_protectors (
    id BIGSERIAL PRIMARY KEY,

    

    part4_id BIGINT NOT NULL     
	REFERENCES part4_master(part4_id)     
	ON DELETE CASCADE,

    protector_type TEXT NOT NULL,          -- Dropdown / Others
    material TEXT NOT NULL,                -- Dropdown / Others

    leg_length_cm NUMERIC
        CHECK (leg_length_cm > 0),

    thickness_cm NUMERIC
        CHECK (thickness_cm > 0),

    height_cm NUMERIC
        CHECK (height_cm > 0),

    load_capacity TEXT,                    -- Dropdown / Others

    colour TEXT,                           -- Dropdown / Others

    quantity_pcs NUMERIC
        CHECK (quantity_pcs > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

--Divider
CREATE TABLE part4_dividers (
    id BIGSERIAL PRIMARY KEY,

    

    part4_id BIGINT NOT NULL     
	REFERENCES part4_master(part4_id)     
	ON DELETE CASCADE,

    divider_type TEXT NOT NULL,            -- Dropdown / Others
    material TEXT NOT NULL,                -- Dropdown / Others

    cell_configuration TEXT,               -- Dropdown / Others

    cell_length_cm NUMERIC
        CHECK (cell_length_cm > 0),

    cell_width_cm NUMERIC
        CHECK (cell_width_cm > 0),

    height_cm NUMERIC
        CHECK (height_cm > 0),

    board_thickness TEXT,                  -- Dropdown / Others
    slot_depth TEXT,                       -- Dropdown / Others

    colour TEXT,                           -- Dropdown / Others

    quantity_pcs NUMERIC
        CHECK (quantity_pcs > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

--Edge Protector
CREATE TABLE part4_edge_protectors (
    id BIGSERIAL PRIMARY KEY,

    

    part4_id BIGINT NOT NULL     
	REFERENCES part4_master(part4_id)     
	ON DELETE CASCADE,

    protector_type TEXT NOT NULL,        -- Dropdown / Others
    material TEXT NOT NULL,              -- Dropdown / Others

    wing_size_cm NUMERIC
        CHECK (wing_size_cm > 0),

    thickness_cm NUMERIC
        CHECK (thickness_cm > 0),

    length_cm NUMERIC
        CHECK (length_cm > 0),

    ply_layers TEXT,                     -- Dropdown / Others
    colour TEXT,                         -- Dropdown / Others

    quantity_pcs NUMERIC
        CHECK (quantity_pcs > 0),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

--Void
CREATE TABLE part4_void_fill (
    id BIGSERIAL PRIMARY KEY,

    

    part4_id BIGINT NOT NULL     
	REFERENCES part4_master(part4_id)     
	ON DELETE CASCADE,

    fill_type TEXT NOT NULL,          -- Air Pillow / Paper Fill / Bubble Wrap / Others
    material TEXT NOT NULL,

    -- ===== Air Pillow specific =====
    pillow_size_cm TEXT,              -- e.g. 200x100
    fill_percent TEXT,                -- Dropdown (e.g. 80%, 90%)

    -- ===== Paper fill specific =====
    paper_type TEXT,
    paper_weight TEXT,                -- GSM or grade

    -- ===== Bubble wrap specific =====
    bubble_size TEXT,
    layer TEXT,                       -- Single / Double / Triple

    -- ===== Common fields =====
    colour TEXT,

    quantity NUMERIC NOT NULL
        CHECK (quantity > 0),

    quantity_unit TEXT NOT NULL
        CHECK (quantity_unit IN ('PCS', 'KGS')),

    surplus_percent NUMERIC
        CHECK (surplus_percent BETWEEN 0 AND 100),

    wastage_percent NUMERIC
        CHECK (wastage_percent BETWEEN 0 AND 100),

    approval_against TEXT,
    remarks TEXT,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

--Authentication
-- 1. organizations
CREATE TABLE organizations (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    owner_name VARCHAR,
    email VARCHAR,
    whatsapp_number VARCHAR,
    location_city VARCHAR,
    location_state VARCHAR,
    industry_vertical VARCHAR,
    plan_tier VARCHAR NOT NULL DEFAULT 'basic' CHECK (plan_tier IN ('basic', 'standard', 'premium', 'enterprise')),
    max_users INTEGER NOT NULL DEFAULT 5,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    subscription_start TIMESTAMP WITH TIME ZONE,
    subscription_end TIMESTAMP WITH TIME ZONE
);

-- 2. users
CREATE TABLE users (
    id UUID PRIMARY KEY,
    organization_id UUID NOT NULL REFERENCES organizations(id),
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    phone VARCHAR,
    password_hash VARCHAR NOT NULL,
    highest_role VARCHAR NOT NULL DEFAULT 'operator' CHECK (highest_role IN ('master_admin', 'admin', 'manager', 'supervisor', 'operator')),
    is_primary_master BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_by UUID REFERENCES users(id),
    last_login TIMESTAMP WITH TIME ZONE
);

-- 3. user_roles
CREATE TABLE user_roles (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    role VARCHAR NOT NULL CHECK (role IN ('master_admin', 'admin', 'manager', 'supervisor', 'operator')),
    department VARCHAR,
    is_default_role BOOLEAN NOT NULL DEFAULT FALSE,
    assigned_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 4. role_permissions
CREATE TABLE role_permissions (
    id UUID PRIMARY KEY,
    user_role_id UUID NOT NULL REFERENCES user_roles(id),
    module VARCHAR NOT NULL,
    permission_level VARCHAR NOT NULL DEFAULT 'none' CHECK (permission_level IN ('none', 'view', 'input', 'edit', 'full', 'config')),
    can_create_users BOOLEAN NOT NULL DEFAULT FALSE,
    can_delete_users BOOLEAN NOT NULL DEFAULT FALSE,
    can_create_roles_up_to VARCHAR CHECK (can_create_roles_up_to IN ('master_admin', 'admin', 'manager', 'supervisor', 'operator') OR can_create_roles_up_to IS NULL)
);

-- 5. permission_requests
CREATE TABLE permission_requests (
    id UUID PRIMARY KEY,
    requested_by UUID NOT NULL REFERENCES users(id),
    module_requested VARCHAR NOT NULL,
    specific_record_id VARCHAR,
    reason TEXT,
    status VARCHAR NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    approved_by UUID REFERENCES users(id),
    expires_at TIMESTAMP WITH TIME ZONE
);

-- 6. audit_log
CREATE TABLE audit_log (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    active_role VARCHAR NOT NULL CHECK (active_role IN ('master_admin', 'admin', 'manager', 'supervisor', 'operator')),
    action_type VARCHAR NOT NULL CHECK (action_type IN ('create', 'edit', 'delete', 'approve', 'login', 'role_switch')),
    module VARCHAR,
    record_id VARCHAR,
    details JSONB,
    ip_address VARCHAR,
    timestamp_audit TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

--UQR 
CREATE TABLE uqr_fabric (
    id BIGSERIAL PRIMARY KEY,

    report_date DATE,
    report_time TIME,
    material_type_description VARCHAR(255),
    quality_checked_by VARCHAR(255),
    approved_by VARCHAR(255),
    invoice_challan_qty DECIMAL(10,2),
    aql_major DECIMAL(5,2),
    aql_minor DECIMAL(5,2),
    uin VARCHAR(100),
    po_no VARCHAR(100),
    factory_po_code VARCHAR(100),
    width_cm DECIMAL(6,2),
    certification_requirement TEXT,

    usn VARCHAR(100),
    fiber_type VARCHAR(255),
    fabric_name VARCHAR(255),
    composition VARCHAR(255),
    gsm DECIMAL(6,2),
    construction_type VARCHAR(255),
    weave_knit_type VARCHAR(255),
    fiber_category VARCHAR(255),
    origin VARCHAR(255),
    fabric_width DECIMAL(6,2),
    fabric_length_meter DECIMAL(10,2),

    defect_type VARCHAR(100),
    defect_at_meter DECIMAL(10,2),
    defect_length DECIMAL(10,2),
    defect_major_count INT DEFAULT 0,
    defect_minor_count INT DEFAULT 0,
    findings TEXT,
    reference_image_path VARCHAR(500),

    moisture_percentage DECIMAL(5,2),
    shade_approval VARCHAR(100),
    result VARCHAR(50),
    remarks TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uqr_yarn (
    id BIGSERIAL PRIMARY KEY,

    report_date DATE,
    report_time TIME,
    material_type_description VARCHAR(255),
    quality_checked_by VARCHAR(255),
    approved_by VARCHAR(255),
    invoice_challan_qty DECIMAL(10,2),
    aql_major DECIMAL(5,2),
    aql_minor DECIMAL(5,2),
    uin VARCHAR(100),
    po_no VARCHAR(100),
    factory_po_code VARCHAR(100),

    usn VARCHAR(100),
    fiber_type VARCHAR(255),
    yarn_type VARCHAR(255),
    yarn_count VARCHAR(100),
    doubling VARCHAR(100),
    ply VARCHAR(100),
    winding VARCHAR(100),
    yarn_weight_found DECIMAL(10,3),
    tpi_twist DECIMAL(10,3),

    defect_type VARCHAR(100),
    defect_major_count INT DEFAULT 0,
    defect_minor_count INT DEFAULT 0,
    findings TEXT,

    avg_weight_difference_found DECIMAL(10,3),
    moisture_percentage DECIMAL(5,2),
    shade_approval VARCHAR(100),
    result VARCHAR(50),
    remarks TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uqr_foam_memory (
    id BIGSERIAL PRIMARY KEY,

    report_date DATE,
    report_time TIME,
    material_type_description VARCHAR(255),
    inspected_by VARCHAR(255),
    approved_against VARCHAR(255),
    invoice_challan_qty DECIMAL(10,2),
    aql_major DECIMAL(5,2),
    aql_minor DECIMAL(5,2),
    uin VARCHAR(100),
    po_no VARCHAR(100),
    factory_po_code VARCHAR(100),

    usn VARCHAR(100),
    foam_type VARCHAR(100),
    subtype VARCHAR(100),
    grade VARCHAR(100),
    color VARCHAR(100),
    thickness DECIMAL(10,2),
    shape VARCHAR(100),
    ild_ifd DECIMAL(10,2),
    fire_retardant VARCHAR(100),
    density DECIMAL(10,2),
    gsm DECIMAL(10,2),
    length_cm DECIMAL(10,2),
    width_cm DECIMAL(10,2),

    certification VARCHAR(255),
    result VARCHAR(50),
    remarks TEXT,
    shape_size_spec VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uqr_foam_pe_epe (
    id BIGSERIAL PRIMARY KEY,

    report_date DATE,
    report_time TIME,
    material_type_description VARCHAR(255),
    inspected_by VARCHAR(255),
    approved_against VARCHAR(255),
    invoice_challan_qty DECIMAL(10,2),
    aql_major DECIMAL(5,2),
    aql_minor DECIMAL(5,2),
    uin VARCHAR(100),
    po_no VARCHAR(100),
    factory_po_code VARCHAR(100),

    usn VARCHAR(100),
    foam_type VARCHAR(100),
    subtype VARCHAR(100),
    color VARCHAR(100),
    thickness DECIMAL(10,2),
    shape VARCHAR(100),
    lamination VARCHAR(100),
    water_resistance VARCHAR(100),
    thermal_insulation VARCHAR(100),
    fire_retardant VARCHAR(100),
    density DECIMAL(10,2),
    gsm DECIMAL(10,2),
    length_cm DECIMAL(10,2),
    width_cm DECIMAL(10,2),

    certification VARCHAR(255),
    result VARCHAR(50),
    remarks TEXT,
    shape_size_spec VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uqr_foam_pu (
    id BIGSERIAL PRIMARY KEY,

    report_date DATE,
    report_time TIME,
    material_type_description VARCHAR(255),
    inspected_by VARCHAR(255),
    approved_against VARCHAR(255),
    invoice_challan_qty DECIMAL(10,2),
    aql_major DECIMAL(5,2),
    aql_minor DECIMAL(5,2),
    uin VARCHAR(100),
    po_no VARCHAR(100),
    factory_po_code VARCHAR(100),

    usn VARCHAR(100),
    foam_type VARCHAR(100),
    subtype VARCHAR(100),
    grade VARCHAR(100),
    color VARCHAR(100),
    thickness DECIMAL(10,2),
    shape VARCHAR(100),
    ild_ifd DECIMAL(10,2),
    support_factor DECIMAL(10,2),
    anti_microbial VARCHAR(100),
    fire_retardant VARCHAR(100),
    density DECIMAL(10,2),
    gsm DECIMAL(10,2),
    length_cm DECIMAL(10,2),
    width_cm DECIMAL(10,2),

    certification VARCHAR(255),
    result VARCHAR(50),
    remarks TEXT,
    shape_size_spec VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uqr_foam_rebonded (
    id BIGSERIAL PRIMARY KEY,

    report_date DATE,
    report_time TIME,
    material_type_description VARCHAR(255),
    inspected_by VARCHAR(255),
    approved_against VARCHAR(255),
    invoice_challan_qty DECIMAL(10,2),
    aql_major DECIMAL(5,2),
    aql_minor DECIMAL(5,2),
    uin VARCHAR(100),
    po_no VARCHAR(100),
    factory_po_code VARCHAR(100),

    usn VARCHAR(100),
    foam_type VARCHAR(100),
    subtype VARCHAR(100),
    chip_source VARCHAR(100),
    chip_size VARCHAR(100),
    bonding VARCHAR(100),
    color VARCHAR(100),
    thickness DECIMAL(10,2),
    shape VARCHAR(100),
    ild_ifd DECIMAL(10,2),
    fire_retardant VARCHAR(100),
    density DECIMAL(10,2),
    gsm DECIMAL(10,2),
    length_cm DECIMAL(10,2),
    width_cm DECIMAL(10,2),

    certification VARCHAR(255),
    result VARCHAR(50),
    remarks TEXT,
    shape_size_spec VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uqr_foam_eva (
    id BIGSERIAL PRIMARY KEY,

    report_date DATE,
    report_time TIME,
    material_type_description VARCHAR(255),
    inspected_by VARCHAR(255),
    approved_against VARCHAR(255),
    invoice_challan_qty DECIMAL(10,2),
    aql_major DECIMAL(5,2),
    aql_minor DECIMAL(5,2),
    uin VARCHAR(100),
    po_no VARCHAR(100),
    factory_po_code VARCHAR(100),

    usn VARCHAR(100),
    foam_type VARCHAR(100),
    subtype VARCHAR(100),
    color VARCHAR(100),
    thickness DECIMAL(10,2),
    shape VARCHAR(100),
    interlocking VARCHAR(100),
    water_resistance VARCHAR(100),
    uv_resistance VARCHAR(100),
    anti_slip VARCHAR(100),
    density DECIMAL(10,2),
    gsm DECIMAL(10,2),
    length_cm DECIMAL(10,2),
    width_cm DECIMAL(10,2),

    shade_approval VARCHAR(100),
    result VARCHAR(50),
    remarks TEXT,
    shape_size_spec VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uqr_foam_gel_infused (
    id BIGSERIAL PRIMARY KEY,

    report_date DATE,
    report_time TIME,
    material_type_description VARCHAR(255),
    inspected_by VARCHAR(255),
    approved_against VARCHAR(255),
    invoice_challan_qty DECIMAL(10,2),
    aql_major DECIMAL(5,2),
    aql_minor DECIMAL(5,2),
    uin VARCHAR(100),
    po_no VARCHAR(100),
    factory_po_code VARCHAR(100),

    usn VARCHAR(100),
    foam_type VARCHAR(100),
    subtype VARCHAR(100),
    gel_type VARCHAR(100),
    gel_content VARCHAR(100),
    color VARCHAR(100),
    thickness DECIMAL(10,2),
    shape VARCHAR(100),
    ild_ifd DECIMAL(10,2),
    cooling_effect VARCHAR(100),
    fire_retardant VARCHAR(100),
    density DECIMAL(10,2),
    gsm DECIMAL(10,2),
    length_cm DECIMAL(10,2),
    width_cm DECIMAL(10,2),

    certification VARCHAR(255),
    result VARCHAR(50),
    remarks TEXT,
    shape_size_spec VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uqr_foam_hr (
    id BIGSERIAL PRIMARY KEY,

    report_date DATE,
    report_time TIME,
    material_type_description VARCHAR(255),
    inspected_by VARCHAR(255),
    approved_against VARCHAR(255),
    invoice_challan_qty DECIMAL(10,2),
    aql_major DECIMAL(5,2),
    aql_minor DECIMAL(5,2),
    uin VARCHAR(100),
    po_no VARCHAR(100),
    factory_po_code VARCHAR(100),

    usn VARCHAR(100),
    foam_type VARCHAR(100),
    subtype VARCHAR(100),
    grade VARCHAR(100),
    color VARCHAR(100),
    thickness DECIMAL(10,2),
    shape VARCHAR(100),
    ild_ifd DECIMAL(10,2),
    support_factor DECIMAL(10,2),
    fire_retardant VARCHAR(100),
    density DECIMAL(10,2),
    gsm DECIMAL(10,2),
    length_cm DECIMAL(10,2),
    width_cm DECIMAL(10,2),

    certification VARCHAR(255),
    result VARCHAR(50),
    remarks TEXT,
    shape_size_spec VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uqr_foam_latex (
    id BIGSERIAL PRIMARY KEY,

    report_date DATE,
    report_time TIME,
    material_type_description VARCHAR(255),
    inspected_by VARCHAR(255),
    approved_against VARCHAR(255),
    invoice_challan_qty DECIMAL(10,2),
    aql_major DECIMAL(5,2),
    aql_minor DECIMAL(5,2),
    uin VARCHAR(100),
    po_no VARCHAR(100),
    factory_po_code VARCHAR(100),

    usn VARCHAR(100),
    foam_type VARCHAR(100),
    latex_type VARCHAR(100),
    natural_content VARCHAR(100),
    subtype VARCHAR(100),
    color VARCHAR(100),
    thickness DECIMAL(10,2),
    shape VARCHAR(100),
    ild_ifd DECIMAL(10,2),
    hypoallergenic VARCHAR(100),
    anti_microbial VARCHAR(100),
    fire_retardant VARCHAR(100),
    density DECIMAL(10,2),
    gsm DECIMAL(10,2),
    length_cm DECIMAL(10,2),
    width_cm DECIMAL(10,2),

    certification VARCHAR(255),
    result VARCHAR(50),
    remarks TEXT,
    shape_size_spec VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uqr_fiber_cotton_fill (
    id BIGSERIAL PRIMARY KEY,

    report_date DATE,
    report_time TIME,
    material_type_description VARCHAR(255),
    inspected_by VARCHAR(255),
    approved_against VARCHAR(255),
    invoice_challan_qty DECIMAL(10,2),
    aql_major DECIMAL(5,2),
    aql_minor DECIMAL(5,2),
    uin VARCHAR(100),
    po_no VARCHAR(100),
    factory_po_code VARCHAR(100),

    usn VARCHAR(100),
    fiber_type VARCHAR(100),
    subtype VARCHAR(100),
    form VARCHAR(100),
    grade VARCHAR(100),
    color VARCHAR(100),
    processing VARCHAR(100),
    bonding VARCHAR(100),
    fire_retardant VARCHAR(100),
    dust_trash_content VARCHAR(100),

    certifications VARCHAR(255),
    result VARCHAR(50),
    remarks TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uqr_fiber_down_alternative (
    id BIGSERIAL PRIMARY KEY,

    report_date DATE,
    report_time TIME,
    material_type_description VARCHAR(255),
    inspected_by VARCHAR(255),
    approved_against VARCHAR(255),
    invoice_challan_qty DECIMAL(10,2),
    aql_major DECIMAL(5,2),
    aql_minor DECIMAL(5,2),
    uin VARCHAR(100),
    po_no VARCHAR(100),
    factory_po_code VARCHAR(100),

    usn VARCHAR(100),
    fiber_type VARCHAR(100),
    subtype VARCHAR(100),
    form VARCHAR(100),
    construction VARCHAR(100),
    denier VARCHAR(100),
    siliconized VARCHAR(100),
    loft_rating VARCHAR(100),
    water_resistance VARCHAR(100),
    hypoallergenic VARCHAR(100),
    anti_microbial VARCHAR(100),
    vegan_cruelty_free VARCHAR(100),

    certifications VARCHAR(255),
    result VARCHAR(50),
    remarks TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uqr_fiber_down_feather (
    id BIGSERIAL PRIMARY KEY,

    report_date DATE,
    report_time TIME,
    material_type_description VARCHAR(255),
    inspected_by VARCHAR(255),
    approved_against VARCHAR(255),
    invoice_challan_qty DECIMAL(10,2),
    aql_major DECIMAL(5,2),
    aql_minor DECIMAL(5,2),
    uin VARCHAR(100),
    po_no VARCHAR(100),
    factory_po_code VARCHAR(100),

    usn VARCHAR(100),
    fiber_type VARCHAR(100),
    bird_type VARCHAR(100),
    form VARCHAR(100),
    origin VARCHAR(100),
    down_percentage VARCHAR(100),
    fill_power VARCHAR(100),
    processing VARCHAR(100),
    odor VARCHAR(100),
    anti_microbial VARCHAR(100),
    cluster_size VARCHAR(100),

    certifications VARCHAR(255),
    result VARCHAR(50),
    remarks TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uqr_fiber_microfiber (
    id BIGSERIAL PRIMARY KEY,

    report_date DATE,
    report_time TIME,
    material_type_description VARCHAR(255),
    inspected_by VARCHAR(255),
    approved_against VARCHAR(255),
    invoice_challan_qty DECIMAL(10,2),
    aql_major DECIMAL(5,2),
    aql_minor DECIMAL(5,2),
    uin VARCHAR(100),
    po_no VARCHAR(100),
    factory_po_code VARCHAR(100),

    usn VARCHAR(100),
    fiber_type VARCHAR(100),
    subtype VARCHAR(100),
    form VARCHAR(100),
    denier VARCHAR(100),
    siliconized VARCHAR(100),
    color VARCHAR(100),
    cluster_size VARCHAR(100),
    anti_microbial VARCHAR(100),
    hypoallergenic VARCHAR(100),
    loft_fill_power VARCHAR(100),
    hand_feel VARCHAR(100),

    certifications VARCHAR(255),
    result VARCHAR(50),
    remarks TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uqr_fiber_polyester_fill (
    id BIGSERIAL PRIMARY KEY,

    report_date DATE,
    report_time TIME,
    material_type_description VARCHAR(255),
    inspected_by VARCHAR(255),
    approved_against VARCHAR(255),
    invoice_challan_qty DECIMAL(10,2),
    aql_major DECIMAL(5,2),
    aql_minor DECIMAL(5,2),
    uin VARCHAR(100),
    po_no VARCHAR(100),
    factory_po_code VARCHAR(100),

    usn VARCHAR(100),
    fiber_type VARCHAR(100),
    subtype VARCHAR(100),
    form VARCHAR(100),
    denier VARCHAR(100),
    siliconized VARCHAR(100),
    color VARCHAR(100),
    bonding VARCHAR(100),
    anti_microbial VARCHAR(100),
    fire_retardant VARCHAR(100),
    loft_fill_power VARCHAR(100),

    certifications VARCHAR(255),
    result VARCHAR(50),
    remarks TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uqr_fiber_speciality_fill (
    id BIGSERIAL PRIMARY KEY,

    report_date DATE,
    report_time TIME,
    material_type_description VARCHAR(255),
    inspected_by VARCHAR(255),
    approved_against VARCHAR(255),
    invoice_challan_qty DECIMAL(10,2),
    aql_major DECIMAL(5,2),
    aql_minor DECIMAL(5,2),
    uin VARCHAR(100),
    po_no VARCHAR(100),
    factory_po_code VARCHAR(100),

    usn VARCHAR(100),
    fiber_type VARCHAR(100),
    source VARCHAR(100),
    properties VARCHAR(255),
    form VARCHAR(100),
    blending VARCHAR(100),
    biodegradable VARCHAR(100),

    certifications VARCHAR(255),
    result VARCHAR(50),
    remarks TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uqr_fiber_wool_natural (
    id BIGSERIAL PRIMARY KEY,

    report_date DATE,
    report_time TIME,
    material_type_description VARCHAR(255),
    inspected_by VARCHAR(255),
    approved_against VARCHAR(255),
    invoice_challan_qty DECIMAL(10,2),
    aql_major DECIMAL(5,2),
    aql_minor DECIMAL(5,2),
    uin VARCHAR(100),
    po_no VARCHAR(100),
    factory_po_code VARCHAR(100),

    usn VARCHAR(100),
    fiber_type VARCHAR(100),
    wool_type VARCHAR(100),
    subtype VARCHAR(100),
    form VARCHAR(100),
    micron VARCHAR(100),
    color VARCHAR(100),
    processing VARCHAR(100),
    lanolin_content VARCHAR(100),
    moisture_wicking VARCHAR(100),
    fire_retardant VARCHAR(100),
    mulesing_free VARCHAR(100),

    certifications VARCHAR(255),
    result VARCHAR(50),
    remarks TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

